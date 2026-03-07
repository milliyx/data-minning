"""Data quality validation rules."""

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from typing import List, Dict, Any


class QualityCheck:
    """Base class for quality checks."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        """
        Run validation and return results.
        
        Returns:
            Dictionary with check results
        """
        raise NotImplementedError


class NotNullCheck(QualityCheck):
    """Check that specified columns have no null values."""
    
    def __init__(self, columns: List[str]):
        super().__init__(
            name="not_null_check",
            description=f"Verify no nulls in columns: {columns}",
        )
        self.columns = columns
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        violations = []
        
        for col in self.columns:
            null_count = df.filter(F.col(col).isNull()).count()
            if null_count > 0:
                violations.append({
                    'column': col,
                    'null_count': null_count,
                })
        
        return {
            'check': self.name,
            'passed': len(violations) == 0,
            'violations': violations,
        }


class RangeCheck(QualityCheck):
    """Check that numeric columns are within expected ranges."""
    
    def __init__(self, column: str, min_val: float, max_val: float):
        super().__init__(
            name=f"range_check_{column}",
            description=f"Verify {column} in range [{min_val}, {max_val}]",
        )
        self.column = column
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        out_of_range = df.filter(
            (F.col(self.column) < self.min_val) |
            (F.col(self.column) > self.max_val)
        ).count()
        
        return {
            'check': self.name,
            'passed': out_of_range == 0,
            'violations': [{
                'column': self.column,
                'out_of_range_count': out_of_range,
            }] if out_of_range > 0 else [],
        }


class UniqueCheck(QualityCheck):
    """Check that specified columns have unique values."""
    
    def __init__(self, columns: List[str]):
        super().__init__(
            name="unique_check",
            description=f"Verify uniqueness of columns: {columns}",
        )
        self.columns = columns
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        total_count = df.count()
        distinct_count = df.select(*self.columns).distinct().count()
        duplicates = total_count - distinct_count
        
        return {
            'check': self.name,
            'passed': duplicates == 0,
            'violations': [{
                'columns': self.columns,
                'duplicate_count': duplicates,
            }] if duplicates > 0 else [],
        }


class ReferentialIntegrityCheck(QualityCheck):
    """Check foreign key relationships."""
    
    def __init__(
        self,
        child_table: str,
        child_column: str,
        parent_df: DataFrame,
        parent_column: str,
    ):
        super().__init__(
            name=f"referential_integrity_{child_table}_{child_column}",
            description=f"Verify {child_table}.{child_column} exists in parent.{parent_column}",
        )
        self.child_column = child_column
        self.parent_df = parent_df
        self.parent_column = parent_column
    
    def validate(self, df: DataFrame) -> Dict[str, Any]:
        # Get distinct values from child
        child_values = df.select(self.child_column).distinct()
        
        # Left anti join to find orphaned records
        orphaned = child_values.join(
            self.parent_df.select(self.parent_column),
            child_values[self.child_column] == self.parent_df[self.parent_column],
            "left_anti"
        ).count()
        
        return {
            'check': self.name,
            'passed': orphaned == 0,
            'violations': [{
                'orphaned_count': orphaned,
            }] if orphaned > 0 else [],
        }


def run_quality_checks(
    table_name: str,
    df: DataFrame,
    checks: List[QualityCheck],
) -> Dict[str, Any]:
    """
    Run all quality checks on a DataFrame.
    
    Args:
        table_name: Name of the table being checked
        df: DataFrame to validate
        checks: List of quality checks to run
        
    Returns:
        Summary of quality check results
    """
    results = {
        'table': table_name,
        'row_count': df.count(),
        'checks': [],
        'all_passed': True,
    }
    
    for check in checks:
        check_result = check.validate(df)
        results['checks'].append(check_result)
        
        if not check_result['passed']:
            results['all_passed'] = False
    
    return results


def print_quality_report(results: Dict[str, Any]) -> None:
    """Print quality check results."""
    print(f"\nQuality Report: {results['table']}")
    print(f"  Row count: {results['row_count']:,}")
    print(f"  Checks run: {len(results['checks'])}")
    print(f"  Status: {'✓ PASSED' if results['all_passed'] else '✗ FAILED'}")
    
    if not results['all_passed']:
        print("\n  Violations:")
        for check in results['checks']:
            if not check['passed']:
                print(f"    - {check['check']}: {check['violations']}")
