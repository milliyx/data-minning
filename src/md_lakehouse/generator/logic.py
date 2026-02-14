"""Business logic for data simulation."""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any


class SimulationEngine:
    """
    Core simulation engine with deterministic business logic.
    
    All randomness is controlled by the seed to ensure reproducibility.
    """
    
    def __init__(self, config: Dict[str, Any], seed: int):
        """
        Initialize simulation engine.
        
        Args:
            config: Simulation configuration parameters
            seed: Random seed for reproducibility
        """
        self.config = config
        self.seed = seed
        self.rng = np.random.RandomState(seed)
        
    def generate_signup_dates(
        self,
        n_users: int,
        start_date: datetime,
        end_date: datetime,
    ) -> List[datetime]:
        """
        Generate user signup dates with slight growth trend.
        
        Args:
            n_users: Number of users to generate
            start_date: Simulation start date
            end_date: Simulation end date
            
        Returns:
            List of signup dates
        """
        days = (end_date - start_date).days
        
        # Generate with slight exponential growth
        raw_days = self.rng.exponential(scale=days/3, size=n_users)
        raw_days = np.clip(raw_days, 0, days)
        
        # Convert to dates
        signup_dates = [
            start_date + timedelta(days=int(d))
            for d in sorted(raw_days)
        ]
        
        return signup_dates
    
    def assign_plans(self, n_users: int) -> List[str]:
        """
        Assign subscription plans based on plan_mix distribution.
        
        Args:
            n_users: Number of users
            
        Returns:
            List of plan names
        """
        plan_mix = self.config['plan_mix']
        plans = list(plan_mix.keys())
        probabilities = list(plan_mix.values())
        
        return self.rng.choice(plans, size=n_users, p=probabilities).tolist()
    
    def assign_demographics(
        self,
        n_users: int,
    ) -> Tuple[List[int], List[str], List[str]]:
        """
        Assign age, city, and acquisition channel.
        
        Args:
            n_users: Number of users
            
        Returns:
            Tuple of (ages, cities, channels)
        """
        age_min = self.config['age_min']
        age_max = self.config['age_max']
        
        # Age distribution (slight skew to younger)
        ages = self.rng.beta(2, 3, size=n_users)
        ages = (age_min + ages * (age_max - age_min)).astype(int).tolist()
        
        # Cities (uniform)
        cities = self.rng.choice(
            self.config['cities'],
            size=n_users,
        ).tolist()
        
        # Acquisition channels (weighted)
        channels = self.rng.choice(
            self.config['acquisition_channels'],
            size=n_users,
            p=[0.3, 0.25, 0.2, 0.15, 0.1],  # organic, paid, social, referral, partnership
        ).tolist()
        
        return ages, cities, channels
    
    def compute_churn_probability(
        self,
        base_rate: float,
        usage_level: float,
        payment_failures: int,
        outage_exposure: float,
        promo_exposure: float,
    ) -> float:
        """
        Compute churn probability based on multiple factors.
        
        Args:
            base_rate: Base monthly churn rate
            usage_level: Normalized usage (0-1, where 1 is high usage)
            payment_failures: Number of recent payment failures
            outage_exposure: Exposure to outages (0-1)
            promo_exposure: Exposure to promotions (0-1)
            
        Returns:
            Churn probability for the period
        """
        # Start with base rate
        prob = base_rate
        
        # Low usage increases churn
        if usage_level < 0.3:
            prob *= 1.5
        elif usage_level < 0.5:
            prob *= 1.2
        
        # Payment failures increase churn
        prob *= (1 + payment_failures * 0.3)
        
        # Outages increase churn
        prob *= (1 + outage_exposure * 0.4)
        
        # Promos decrease churn
        prob *= (1 - promo_exposure * 0.2)
        
        return min(prob, 0.95)  # Cap at 95%
    
    def compute_usage_level(
        self,
        plan: str,
        day_of_week: int,
        promo_active: bool,
        outage_active: bool,
        seasonality_strength: float,
    ) -> Tuple[int, float]:
        """
        Compute daily usage (sessions and minutes).
        
        Args:
            plan: Subscription plan
            day_of_week: Day of week (0=Monday, 6=Sunday)
            promo_active: Whether a promo is active
            outage_active: Whether an outage occurred
            seasonality_strength: Seasonality effect strength
            
        Returns:
            Tuple of (sessions, minutes)
        """
        # Base usage by plan
        base_sessions = {'basic': 2, 'standard': 4, 'premium': 6}
        base_minutes = {'basic': 30, 'standard': 60, 'premium': 120}
        
        sessions = base_sessions[plan]
        minutes = base_minutes[plan]
        
        # Weekend boost
        if day_of_week >= 5:  # Saturday or Sunday
            weekend_boost = 1 + seasonality_strength
            sessions *= weekend_boost
            minutes *= weekend_boost
        
        # Promo boost
        if promo_active:
            sessions *= self.config['promo_impact']
            minutes *= self.config['promo_impact']
        
        # Outage penalty
        if outage_active:
            sessions *= (1 - self.config['outage_impact'])
            minutes *= (1 - self.config['outage_impact'])
        
        # Add noise
        sessions = max(0, int(sessions * self.rng.normal(1, 0.2)))
        minutes = max(0, minutes * self.rng.normal(1, 0.25))
        
        return sessions, minutes
    
    def compute_payment_success(
        self,
        base_fail_rate: float,
        price_sensitivity: float,
        plan_price: float,
        outage_active: bool,
    ) -> bool:
        """
        Determine if a payment succeeds.
        
        Args:
            base_fail_rate: Base payment failure rate
            price_sensitivity: Price sensitivity factor
            plan_price: Price of the plan
            outage_active: Whether an outage occurred recently
            
        Returns:
            True if payment succeeds
        """
        fail_rate = base_fail_rate
        
        # Higher prices increase failure rate
        fail_rate *= (1 + price_sensitivity * (plan_price / 20.0))
        
        # Outages increase payment failures
        if outage_active:
            fail_rate *= 1.5
        
        return self.rng.random() > fail_rate
