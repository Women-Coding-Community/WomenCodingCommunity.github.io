[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]

# Welcome to Women Coding Community :sparkles: :computer:

The Women Coding Community is a community dedicated to inspiring women to excel in their technology careers. Our events cover various topics around software engineering.
If you're interested in joining the community as a member or volunteer please visit our [website](https://womencodingcommunity.com/) or join [our Slack](https://join.slack.com/t/womencodingcommunity/shared_invite/zt-2hpjwpx7l-rgceYBIWp6pCiwc0hVsX8A).

Check out [Code of Conduct]([https://WomenCodingCommunity.github.io/code-of-conduct/](https://womencodingcommunity.com/code-of-conduct)

# About

Please, find more information on our [website](https://womencodingcommunity.com).

# Contributing

This website acts as a project to help introduce people to the Open Source community, and allow transition from newcomers to contributors easier.

We welcome your contributions! 💕 To contribute to this repo, follow the [contributing guidelines](CONTRIBUTING.md).

# About our project

## How to Run Project Locally

This content is created using GitHub Pages with Jekyll.

### Prerequisites

Before you can use Jekyll to test a site, you must:

1. Install [Jekyll](https://jekyllrb.com/docs/installation/).
Create a Jekyll site. For more information, see "Creating a GitHub Pages site with Jekyll."
We recommend using Bundler to install and run Jekyll. Bundler manages Ruby gem dependencies, reduces Jekyll build errors, and prevents environment-related bugs. To install Bundler:

2. Install Ruby. For more information, see [Installing Ruby](https://www.ruby-lang.org/en/documentation/installation/).

3. Install Bundler. For more information, see [Bundler](https://bundler.io/)

### [Build and run](#build-and-run)

- Run on terminal `bundle install`

- Run on terminal `bundle exec jekyll serve`

- Access the page on browser: http://127.0.0.1:4000

### Run Tests Locally

* Javascript Tests
- Run on terminal `npm install`
- Run on terminal `npm test`

* Python Tests

```shell script
  cd tools 
  ls -lah
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  pytest tools
```


### External Links about GitHub Pages

* [GitHub Pages Doc](https://docs.github.com/en/pages)
* [About GitHub Pages and Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)
* [Test locally with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)


## How to Troubleshoot Building Project Locally

The project requires to use ruby>=3.1.*. Make sure that your system looks at the correct version of ruby.

### Possible errors
![Bundler error](https://i.ibb.co/mJ8N9fk/image.png) after ```bundle install``` command.


### Setup ruby with rbenv
* First, check which path of ruby you have. If it's incorrect or missing, set it.
```
env | grep PATH

export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
```
To install the correct ruby version, use the following command:

```
rbenv install 3.1.2
```
* Set the 3.1.* version of ruby as the default one globally or only for your working directory.
```
rbenv global 3.1.2  # set the default Ruby version for this machine
# or:
rbenv local 3.1.2   # set the Ruby version for this directory
```

* Get back to the [Build and run](#build-and-run) section.

### Remove Gemfile.lock

As an alternative way, remove Gemfile.lock if setting Ruby version didn't help.

## How to Run End-To-End Testing Locally

1. Open your Terminal in the root directory.
2. `npm install cypress --save-dev` - This will install Cypress locally as a dev dependency for your project.
3. Run `npx cypress open` from your project root
4. Select E2E testing

![Open Cypress](https://i.ibb.co/4VNPFjf/welcome-cypress.png)

5. Select *E2E testing* option.

6. Choose your browser and click *Start E2E testing in..*..

![Browser Selection](https://i.ibb.co/kQxJpmJ/browser-selection.png)

Now you can run any tests from *Specs*.

For more details, please refer to the official [Cypress Documentation](https://docs.cypress.io/guides/overview/why-cypress).


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/WomenCodingCommunity/WomenCodingCommunity.github.io?style=flat-square
[contributors-url]: https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/WomenCodingCommunity/WomenCodingCommunity.github.io?style=flat-square
[forks-url]: https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/network/members
[stars-shield]: https://img.shields.io/github/stars/WomenCodingCommunity/WomenCodingCommunity.github.io?style=flat-square
[stars-url]: https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/stargazers
[issues-shield]: https://img.shields.io/github/issues/WomenCodingCommunity/WomenCodingCommunity.github.io?style=flat-square
[issues-url]: https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/issues/
