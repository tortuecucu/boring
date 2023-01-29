from src.pipeline import Schema, PipelineFactory

s = Schema.schema('titanic')
factory = PipelineFactory()
p = factory.pipeline(s)
...