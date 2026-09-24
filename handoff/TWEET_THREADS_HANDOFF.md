# Project: Turning my Twitter threads into Quarto blog posts

Context carried over from a claude.ai conversation. I'm Christopher Hanusa (@mathzorro).

## Goal
Turn threads I wrote on Twitter into blog posts on my Quarto website, one post per thread
(or a few related threads merged into one post).

## Rules for each post
- **Do not change any of my text.** Only combine the tweets, in order, into one post.
- Allowed formatting fixes only: decode HTML entities (`&gt;` → `>`), replace t.co links
  with their expanded URLs as Markdown links, remove t.co links that only point to
  attached media, and keep intentional line breaks (use code blocks for notation such
  as two-line permutation notation).
- Include every image from the thread. Images are in the archive at
  `data/tweets_media/<tweet_id>-<media_name>.jpg`. Copy them into the post's folder.
- Match the front matter and folder structure of my existing posts in this repo.
- Add a one-line note at the top linking to the original thread (optional; ask me).

## Tools
- `extract_threads.py <archive_folder>` rebuilds all my self-authored threads from
  `data/tweets*.js` and writes `threads.json`, including each tweet's cleaned text and
  the matching file in `data/tweets_media/`.
- My archive has 6,271 tweets and 89 self-authored threads.

## Done
- **Multiplying permutations with string diagrams** (May 10, 2020, 8 tweets, root id
  1259537489393524737). Draft is in `multiplying-permutations/index.qmd`. Still needed:
  copy its 3 images from the archive, match my front matter, render and check.

## Candidates, in rough priority order (root tweet ids)
1. Juggling and Kostant's partition function (Jan 13, 2020, 11 tweets): 1216710644013113344
2. Mathematical Design course, Desmos + AxiDraw. Merge: 1306354402505224192 (Sep 2020),
   1618326275223089152 (Jan 2023, 16 tweets), 1706126524036808928 (Sep 2023 talk)
3. Apollonian jewelry. Merge: 1248656214478766081, 1256217632824528897, 1256545927990595584
4. Streamlines sculptures, JMM 2022 (my most-liked thread): 1469673726295879682;
   optionally with "Existence and Uniqueness" solo show: 1500110527695052801
5. Riemondrian and calculus art: 1535452653928472582
6. Packing 16 tetrahedra in Mathematica: 1577495580858875904
7. Peer praise as a teaching practice. Merge: 1208133033422999554, 1334268144211398658
8. Flipped classroom in Discrete Math. Merge: 1589723953068937217, 1589798640545325056
9. Small pieces: palindrome day 12321 (1352972822432411648), experimental mathematics
   blurb (1041863238168838145), alternating billiards paper (1082470898869903366),
   parametric-to-polar Desmos trick (1412353674098229249)

Note: several candidates are replies to other people (they start with @handles).
Ask me how to handle those leading mentions before stripping or keeping them, since
the rule is not to change my text.
