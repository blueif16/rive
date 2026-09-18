import WorldModelFigure from './figure/WorldModelFigure';
import './article.css';

export default function Article() {
  return (
    <main className="essay">
      <header className="essay-head">
        <p className="essay-kicker">Research note</p>
        <h1 className="essay-title">What a world model is for</h1>
        <p className="essay-byline">Figure study · bake-off · React + DOM/SVG/CSS</p>
      </header>

      <p>
        The phrase <i>world model</i> gets used as though it named a single artefact, but
        in practice it names a capability that can be pointed in several directions. The
        same learned dynamics can be asked for a picture of what happens next, for the
        number that a sensor would read, or for the move a body should make. These are not
        three implementations of one interface; they are three different questions, and
        the shape of the answer differs in each case.
      </p>

      <figure className="essay-figure">
        <WorldModelFigure />
      </figure>

      <p>
        Read the figure from the output backwards. A <b>renderer</b> is judged on
        appearance: it emits a stream of frames, each a complete picture, and the fidelity
        of any single frame is what matters. A <b>simulator</b> is judged on a trajectory:
        it emits a quantity that has a value at every instant, and the thing you compare
        against the world is the whole curve, not one point on it. A <b>planner</b> is
        judged on a commitment: it emits a choice drawn from a finite vocabulary, and
        between choices there is nothing to interpolate.
      </p>

      <p>
        The distinction matters because the failure modes do not transfer. A renderer that
        drifts produces a plausible film of a world that is not this one. A simulator that
        drifts produces a number that is confidently wrong at every timestep. A planner
        that drifts picks the wrong action and then has to live in the world its choice
        created. Evaluating all three with the same metric — pixel error, say, or one-step
        likelihood — quietly assumes they are the same kind of object, and they are not.
      </p>
    </main>
  );
}
