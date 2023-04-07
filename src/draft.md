for AI
each time:
card state of other players
 - observable
 - unobservable
which needs an class named
```python
import torch
from torch.nn import functional as F
def encode(card) -> torch.Tensor:
    pass
# ---
class CardState:
    """
    of gameState of card set
    """
    probabilistic_encoding:torch.Tensor
    
class ObservedCardState(CardState):
    cards: list
    probabilistic_encoding = torch.vstack(
        # deterministic
        [F.one_hot(encode(card_i)) for card_i in cards]
    )

class UnobservedCardState(CardState):
    pass

```

those two sub-classes are used in 
```python
class Game:
    pass
class ObservedGame(Game):
    pass
class UnobservedGame(Game):
    pass
```

the probability of card set cannot reflect all information
hence we need another embedding vector
probability alone is enough to determine
embedding vector(markov state) 
-> probability(as similar as possible to true card set) 
-> decision

a class named CardSet for true card set for each player may be used
and for 


for general core:

pile()
draw()


core api for train and test should be separated
train:
true state is available (not for agent but for trainer)
test:
true state is not available

```python
class Trainer:
    pass
```
train: the training for encoder and decider can be separated
and can be cotrained, also.
trainer is specified for agent
agent.train(trainingG
agent.play(Realgame)

perhaps we donot need a uniform api for trainer
of different structure of agents

for predicter-decider agent:
agent.load_prd(...pt)
agent.load_dcd(...pt)






