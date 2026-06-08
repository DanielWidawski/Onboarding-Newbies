from orders.order_validator import EmptyOrderValidator, OrderValidatorManager


default_validator_manager = OrderValidatorManager([EmptyOrderValidator()])