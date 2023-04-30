# Indy Survey Tool<!-- omit from toc -->

This is the repository for Indy Survey Tool, a framework to unearth correlations in survey data. Our framework allows for easily importing papers, and creates a beautiful companion webpage for your survey, with visualizations and filtering tools which are customizable to your needs. The webpage allows anyone to submit information about new papers to be included in the survey, in order to keep data relevant even after publication.

Survey webpages built using Indy Survey Tool: [Sara's survey, David's survey]

## Table of Contents<!-- omit from toc -->

- [Getting Started](#getting-started)
- [Running the Webpage](#running-the-webpage)
  - [`npm install`](#npm-install)
  - [`npm run prepare`](#npm-run-prepare)
  - [`npm run dev`](#npm-run-dev)
- [Uploading Survey Papers](#uploading-survey-papers)
  - [Upload in Bulk](#upload-in-bulk)
  - [Manually Upload Paper](#manually-upload-paper)
  - [Adding a New Paper Categorization](#adding-a-new-paper-categorization)
- [Configuring the Webpage](#configuring-the-webpage)
  - [Overview of survey-config.json](#overview-of-survey-configjson)
  - [Adding a Filter Group](#adding-a-filter-group)
  - [Modifying the Paper Detail View](#modifying-the-paper-detail-view)
  - [Modifying the Paper Summary View](#modifying-the-paper-summary-view)
  - [Modifying the Title \& Top Panel Information](#modifying-the-title--top-panel-information)
  - [Modifying the Webpage Color](#modifying-the-webpage-color)
  - [Linking to Other Surveys](#linking-to-other-surveys)

## Getting Started

To create your survey webpage:

1. Fork the repo by clicking "Fork" near the top right of the GitHub interface.

2. Clone your new repository to your local machine. E.g., in your terminal / command prompt `CD` to where you want this the folder for the repo to be. Then run

    ```bash
    git clone <THE_NEW_REPO_URL>
    ```

    `CD` or open a terminal / command prompt window into the cloned folder.

## Running the Webpage

In the project directory, you can run:

### `npm install`

Install all the libraries you need to get the app running using the list from `package.json`.

### `npm run prepare`

Run this command prior to `npm run dev` to update the webpage with any changes.

### `npm run dev`

Runs the site locally in development mode.<br />
It should provide a link to localhost to view the site in your browser.

## Uploading Survey Papers

The easiest method of uplaoding survey papers in bulk is using our CSV converter, but it is also possible to add papers individually.

### Upload in Bulk

1. Export your list of survey papers in CSV format. E.g.:
   * In Zotero, right-click the collection -> "Export Collection" -> Format: "CSV"
   * In Airtable, under the name of the view select "Download CSV"
   * In Notion, click the ... icon -> "Export" -> Export format: "Markdown & CSV"
2. Save the file to the root directory of this project with the name [Survey-Info.csv](Survey-Info.csv).
3. Edit the headers of the CSV file, if necessary. Note that at a minimum, `Name`, `Year`, `Authors` (comma separated), `DOI`, and `Bibtex` are required. Make sure the headers match exactly. See [Adding a New Paper Categorization](#adding-a-new-paper-categorization) for more information about defining more categories for the papers.
4. Run the following code to generate a file named [survey-data.json]().
    ```bash
    python3 convertCSVtoJson.py
    ```
5. Move this file to [src/data](src/data) for the webpage to display the papers. This is to allow you to make updates to the file without any previous changes being overwritten.

### Manually Upload Paper

To add papers one-by-one, open [src/data/survey-data.json](src/data/survey-data.json). Then, add a new paper object to the list under the `"data"` tag using the template below as a guide. Note that the `"Name"`, `"Year"`, `"Authors"`, `"DOI"`, and `"Bibtex"` tags are required, but more can be added.
```json
"data": [  // array of paper objects
    {
        "Name"   : "[Poster] Visualization of solar radiation data in augmented reality",
        "Year"   : "2014",
        "Bibtex" : "'@INPROCEEDINGS{6948437,\n  author={Beatriz Carmo, Maria and Cl\u00e1udio, ....",
        "DOI"    : "10.1109/ISMAR.2014.6948437",
        "Authors": [
            "M. Beatriz Carmo; A. P. Cl\u00e1udio; A. Ferreira; A. P. Afonso; ...."
        ]
    },
]
```

### Adding a New Paper Categorization

If your survey papers are categorized by some tag, `<NEW_TAG>`, you should follow these steps to ensure it is displayed properly on the webpage:

1. Open [src/data/survey-data.json](src/data/survey-data.json).
2. Under `"meta"`, add a new object defining the properties of this tag:
    ```json
        {
            "name": "NEW_TAG",
            "type": "MultiSelect"  // categorization type: String or MultiSelect
        },
    ```
    Note that the type of the tag affects what a user of your webpage sees when they go to add a new paper using the "Add Entry" button at the top right. `String` allows the user to enter a string, whereas `MultiSelect` gives the user a dropdown of options to choose from. The options will be all the values in current papers.
3. Add the same information to the `includeProp` dictionary at the top of [convertCSVtoJson.py](convertCSVtoJson.py) if you intend to use the [bulk paper import](#upload-in-bulk) method.

## Configuring the Webpage

Many aspects of the webpage, including colors, filter groups, tags on papers, and displayed icons are fully customizable.

### Overview of survey-config.json

[src/data/survey-config.json](src/data/survey-config.json) contains most of the configuration options for the webpage. It is structured as follows:

```json
{
    "filterBy"   : [],  // defines custom categories that can be used to filter the papers
    "detailView" : [],  // information displayed when a paper is clicked by the user
    "summaryView": [],  // information displayed in the paper view center panel
    "topView"    : []   // information displayed in the top panel of the webpage
}
```

### Adding a Filter Group

Filter groups are comprised of parts of one or more paper categories. These filter groups are used to control the axes for the matrix visualization on the right-hand panel. In [src/data/survey-config.json](src/data/survey-config.json), under `"filterBy"`, add a new object to the list defining the group, e.g.:
```json
    {
        "groupName": "Theory and Contribution",
        "categories":
        [
            {
                "name": "Opportunity",
                "values": [
                    "Engagement",
                    "Collaboration",
                    "Situated Analytics",
                    "Embodied Data Exploration",
                    "Spatial Immersion",
                    "Multi-Sensory Presentation"
                ]
            },
            {
                "name": "Contribution Type",
                "values": [
                    "Technique",
                    "Evaluation",
                    "Design Study",
                    "System"
                ]
            }
        ]
    },
```

* `"groupName"` will be the name displayed for the group on the left panel
* `"categories"` is a list of objects, where each object has:
  * `"name"`, a paper categorization property defined in `"meta"`—see [adding a new paper categorization](#adding-a-new-paper-categorization)
  * `"values"`, an array of strings which are possible values for the property `"name"`

### Modifying the Paper Detail View

To change what is displayed when a user clicks on a specific paper, open [src/data/survey-config.json](src/data/survey-config.json) and navigate to the `"detailView"` tag. Under `"show"`, a list of paper properties to be displayed when the paper is clicked can be provided. By default, the following properties are shown:

* Title
* Short Title
* Authors
* Year
* DOI
* BibTeX

### Modifying the Paper Summary View

To change what is displayed in the central panel paper view, open [src/data/survey-config.json](src/data/survey-config.json) and navigate to the `"summaryView"` tag. Under `"show"`, a list of paper properties to be displayed when the paper is clicked can be provided. By default, only title and authors are shown.

### Modifying the Title & Top Panel Information

Open [src/data/survey-config.json](src/data/survey-config.json) and navigate to the `"topView"` tag. Here, important information displayed in the top panel can be modified:

* `"title"`: title of the survey displayed at the top of the webpage
* `"description"`: survey description
* `"authors"`: survey authors
* `"addEntry"`:
  * `"description"`: text displayed at the top of the Add Entry window
  * `"github"`: link to the survey GitHub repository, where users may open a GitHub issue to request that a paper be added

### Modifying the Webpage Color

To change the color palette of the webpage, open [src/theme/_smui-theme.scss](src/theme/_smui-theme.scss). The `$primary` and `$secondary` variables are the colors used for interactive elements of the webpage like buttons and the time range selector. The `$surface` and `$background` variables are the color of the surface elements and the page background.

### Linking to Other Surveys

Links to other surveys can be added, which appear when users click on the "Other Surveys" option at the top right of the webpage. To add a survey, open [src/data/other-surveys.json](src/data/other-surveys.json) and add a new object, with the name of the survey and a link to the webpage.