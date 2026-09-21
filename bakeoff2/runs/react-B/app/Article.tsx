import Figure from './figure/Figure';
import './article.css';

/**
 * The demo page. Its only job is to put the figure in a realistic context —
 * an essay column with prose above and below it.
 */
export default function Article() {
  return (
    <main className="article">
      <p className="kicker">Research note</p>
      <h1>The ground under its feet</h1>
      <p className="byline">Why an optimiser's starting point decides where it ends up.</p>

      <p>
        Training a model is a descent. At every step the optimiser measures the
        slope of the loss where it currently stands and takes a step downhill.
        That is the whole procedure, and the thing worth noticing is how little
        it knows: not the shape of the landscape, not where the lowest point is,
        only the tilt of the ground directly underfoot.
      </p>

      <Figure />

      <p className="caption">
        <strong>Caption.</strong> A one-dimensional loss landscape with two
        valleys. Gradient descent follows the local slope and settles in
        whichever valley it happens to fall into — so the same procedure on the
        same landscape gives different answers from different starting points,
        and reshaping the landscape moves the answer again.
      </p>

      <p>
        This is why initialisation is a real design decision rather than
        bookkeeping, and why a loss that reports a comfortable number is not by
        itself evidence that the optimiser found anything. A basin can be
        locally perfect and globally mediocre. The descent has no way to tell
        the difference, because from inside a valley every direction is uphill.
      </p>
    </main>
  );
}
