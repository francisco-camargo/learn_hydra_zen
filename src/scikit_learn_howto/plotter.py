"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#gathering-and-visualizing-the-results
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from pathlib import Path


def main():
    
    images = sorted(
        Path("multirun/").glob("**/*.png"),
        # sort by dataset name
        key=lambda x: str(x.name).split(".png")[0].split("_")[0],
    )

    fig, ax = plt.subplots(
        ncols=10,
        nrows=3,
        figsize=(18, 4),
        tight_layout=True,
        subplot_kw=dict(xticks=[], yticks=[]),
    )

    for i, image in enumerate(images):
        dname, cname = image.name.split(".png")[0].split("_", 1)
        image = str(image)

        img = mpimg.imread(image)

        row = i // 10
        col = i % 10
        # ax[row, col].set_axis_off()
        ax[row, col].imshow(img)

        if row == 0:
            ax[row, col].set_title(cname)

        if col == 0:
            ax[row, col].set_ylabel(dname)

    plt.show()


if __name__ == '__main__':
    main()