import Figure from './figure/Figure';
import './article.css';

/**
 * The demo page. Its only job is to put the figure in a realistic context —
 * an essay column with prose above and below it. Replace the placeholder
 * paragraphs with two or three that suit the figure's subject.
 */
export default function Article() {
  return (
    <main className="article">
      <p className="kicker">Research note</p>
      <h1>Figure title</h1>
      <p className="byline">Placeholder essay page for the embedded figure.</p>

      <p>
        Replace this paragraph with prose that sets up the figure. The figure
        below should read as an illustration of the argument, not as decoration
        dropped between sections.
      </p>

      <Figure />

      <p className="caption">
        <strong>Caption.</strong> One or two sentences naming what the figure
        shows, so the point survives without the animation.
      </p>

      <p>
        Replace this paragraph with prose that follows on from the figure,
        picking up the idea it illustrated and carrying it forward.
      </p>
    </main>
  );
}
