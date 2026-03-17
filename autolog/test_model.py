from autolog.agent.agent import AgentCore
from autolog.agent.backend import get_backend

backend = get_backend()
agent = AgentCore(backend)

for i in range(3):
    entry = agent.create_entry(
        raw_note=""" All activations have an impact on performance.
The convolution activation seems to have the largest impact on convergence speed.
convolution + softplus seems to have to largest impact on overall performance.
Full photonic model has the worst performance.
**NOTE**: 'gate+softplus' and 'gate+convolution' have the same performance as 'gate', 'conv' and 'softplus' alone. 

    """,
    timestamp='2026-03-15T10:00:00Z'
    )
    
    print(entry)