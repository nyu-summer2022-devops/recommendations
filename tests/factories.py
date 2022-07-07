import factory
import faker_commerce
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from service.models import Recommendation, Type

factory.Faker.add_provider(faker_commerce.Provider)

class RecommendationFactory(factory.Factory):
    class Meta:
        model = Recommendation

    id = factory.Sequence(lambda n: n)
    product_id = factory.Sequence(lambda n: n)
    product_name = factory.Faker('ecommerce_name')
    rec_id = factory.Sequence(lambda n: n)
    rec_name = factory.Faker("ecommerce_name")
    rec_type = FuzzyChoice(choices=[Type.CROSS_SELL, Type.UP_SELL, Type.ACCESSORY, Type.BUY_WITH])
