# Contributing Guidelines
---


Firstly thanks for your contributions!!! :sparkling_heart::sparkling_heart:   

If you have resources you would like to share from your event or resources you think our community would benefit from keep reading!

## PRE-REQUISITE

1. 📖 Read up on fork & pull request models
2. 🍴 Fork this repo to your account
3. 🌱 Create a branch for the change you intend to make in your fork
4. ✍️ Make your changes to the above created branch in your fork
5. 🔨 Follow the contributing guidelines below
6. 🔧 Send a pull request from your fork's branch to our `master` branch
7. :running_woman: Share your PR with the code owners on Slack
8. 🎉 Get your pull request approved - success!

## ⭐ How To Make A Pull Request:

**1.** Start by making a Fork of the [**Women Coding Community**](https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io) repository. Click on the <a href="https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/fork"><img src="https://i.imgur.com/G4z1kEe.png" height="21" width="21"></a>Fork symbol at the top right corner.

**2.** Clone your new fork of the repository in the terminal/CLI on your computer with the following command:

```bash
git clone https://github.com/<your-github-username>/london
```

**3.** Navigate to the newly created LinkFree project directory:

```bash
cd london
```



**4.** Create a new branch:

```bash
git checkout -b YourBranchName
```

**5.** Sync your fork or your local repository with the origin repository:

- In your forked repository, click on "Fetch upstream"
- Click "Fetch and merge"

### Alternatively, Git CLI way to Sync forked repository with origin repository:

```bash
git fetch upstream
```

```bash
git merge upstream/main
```
### Additional way to Sync forked repository with origin repository using Git CLI:

```bash
git remote add wcc git@github.com:WomenCodingCommunity/WomenCodingCommunity.github.io.git
```

```bash
git checkout origin main
```

```bash
git pull wcc main
```

```bash
git push origin main
```

```bash
git checkout -b create_my_new_branch_from_main
```

#### Check out the [Github Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork) to learn more about syncing a forked repository.

**6.** Make your changes to the source code.

**7.** Stage your changes and commit:
```bash
git add <file/folder>
```

```bash
git commit
```

**8.** Push your local commits to the remote repository:

```bash
git push origin YourBranchName
```

**9.** Create a [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)!

**10.** **Congratulations!** You've made your first contribution to [**WCC-London**](https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io)! 🙌🏼

**_:trophy: After this, the maintainers will review the PR and will merge it if it helps move the project forward. Otherwise, it will be given constructive feedback and suggestions for the changes needed to add the PR to the codebase._**



## Find something to work on

The first step to getting starting contributing is to find something
to work on. Help is always welcome, and no contribution is too small!

Here are some things you can do today to get started contributing:

1. You can browse the issues labeled as [help wanted](https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) and [good first issue](https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) to see who is looking for help.

The `good first issue` label also indicates that Women Coding Community - London Members have committed to providing extra assistance for newcontributors.

## Code Pattern Guide :memo:
- Use single quotes pattern for simple strings. (Example: `const containerEl = jQuery('#container')` instead of `const containerEl = jQuery("#container")`)
- Define constants that may be used multiple times ahead, and with uppercase variables. Example:
```
const MENTOR_TYPE_BOTH = 'both';

...

if (someValue === MENTOR_TYPE_BOTH) {
    ...
}
```

- Consider defining variables and functions with `const` instead of `let` for declarations that should not change.

## Style Guide for Git Commit Messages :memo:

**How you can add more value to your contribution logs:**

- Use the present tense. (Example: "Add feature" instead of "Added feature")
- Use the imperative mood. (Example: "Move item to...", instead of "Moves item to...")
- Limit the first line (also called the Subject Line) to _50 characters or less_.
- Capitalize the Subject Line.
- Separate subject from body with a blank line.
- Do not end the subject line with a period.
- Wrap the body at _72 characters_.
- Use the body to explain the _what_, _why_, _vs_, and _how_.

## Best practices

- Write clear and meaningful git commit messages.
- If the PR will *completely* fix a specific issue, include `fixes #123` in the PR body (where 123 is the specific issue number the PR will fix. This will automatically close the issue when the PR is merged.
- Make sure you don't include `@mentions` or `fixes` keywords in your git commit messages. These should be included in the PR body instead.
- When you make a PR for small change (such as fixing a typo, style change, or grammar fix), please squash your commits so that we can maintain a cleaner git history.
- Make sure you include a clear and detailed PR description explaining the reasons for the changes, and ensuring there is sufficient information for the reviewer to understand your PR.
- Additional Readings:
    - [chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/)
    - [github.com/blog/1506-closing-issues-via-pull-requests ](https://github.com/blog/1506-closing-issues-via-pull-requests)
    - [davidwalsh.name/squash-commits-git ](https://davidwalsh.name/squash-commits-git)


## Reporting issues OR suggesting changes/features to the existing repo:

1. In order to discuss changes, you are welcome to [open an issue](https://github.com/WomenCodingCommunity/WomenCodingCommunity.github.io/issues/new/choose) about what you would like to contribute. Enhancements are always encouraged and appreciated.
2. A repository owner will review the issue and provide feedback.

## All the best! 🥇
