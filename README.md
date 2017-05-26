# River Physics Test

## Intent
To test out some basic water physics to be implemented in Unity, I created this python playground to test out how to simulate water moving through a 'river'.

## Setup
If you have an odd desire to work with my toy code, here you go. Just follow the steps.

```
# First time setup
git clone ...
cd river-demo
pip install -r requirements.txt

# Run the script
python main.py
```

## Status
Currently, the river flows upside down because I have yet to build a mapping between the model coordinates and render coordinates. Besides that, it works, but with no source or sink of water - it's more a lake simulator than a river.

It's answered the critical questions that I've been curious about and helped me work out some physics kinks in 2D before going for 3D.

Here it is in action:
![River Demo in Action](https://github.com/ManickYoj/river-demo/blob/master/docs/iteration_01.gif?raw=true)

## Possible Future Work
- Engine: The simulation sits on a cute, underpowered pygame-based engine which I may extend for future simulations or small 2D games. Fixing it up just a little would make the river right side up, which would be nice.
- Momentum: It turns out that water needs momentum to work properly. Right now, it doesn't have it. I hack around the problem by keeping some water in place so it doesn't form unstable waves, but a better implementation would be nice.
