from src.pipeline import Schema, PipelineFactory

s = Schema.schema('test_pipe')
factory = PipelineFactory()
p = factory.pipeline(s)
...