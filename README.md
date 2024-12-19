# fluentix: v0.0.1 pre-alpha

Official fluentix's repo.

[![N|Solid](https://cdn.prod.website-files.com/674856bff10105193a1e4dd4/6748583d409715928ff42120_fluentix-white.png)](https://fluentix.dev)

**Below is a poorly made documentation, please stay tuned because Fluentix project is still in very early development.**

**Visit our [official documentation](https://docs.fluentix.dev) page to see available resources.**

**Discord: https://discord.gg/mZNNfuMUVq**

---

## Features (at this moment):

Features that Fluentix has.

### Fluentix Language

- Variables declarations (array, string, list, nums)
- Equations solved
- `Show` (print) function
- `Input` / `ask` function
- Basic conditions check.

### Fluentix Syntax

**Data types**

Currently, we only support number, string, null, array and boolean
For example: true represents the normal true value for almost every programming language. Same for false
null represents null in almost every programming language
Strings can be used between `'` and `"` just like any other languages.
Array starts with a `[` and ends with `]`. To seperate elements, we use `;`.

**ARRAY TIPS**

You can spam as much `;` as you can when seperating elements in an array. Below shows the reference:

```
let a be [1;;;;;;;;;;;;;;2;;;;;;;;;;;;;;;;;;;;;;;;;;;;3]
```

And it still gonna work.

**Variables**

To declare a variable, we introduce 7 different ways of doing it:

```
variable <var_name> is <value>
let <var_name> be <value> (the most used one)
constant <var_name> is <value>
create: variable <var_name> is <value>
create: constant <var_name> is <value>
create: changeable <var_name> is <value>
create: unchangeable <var_name> is <value>
```
To update a variable, we use: `<var_name> is now <value>`

Way number 1, 2, 4, 6 creates a mutable variable while way number 3, 5, 7 creates a constant.

**Conditions**

To check for something equalivent to something, greater or less than (math):

```
let a be tonumber: ask: "Enter Number: "

if a = 5
    show: "a is 5"

unless a < 5
    show: "a is less than 5"

else
    show: "a is greater than 5"
```

Those are the basics.

*Usages for Conditions*

You can start the check by typing:

```
if <what to check>
    <do something>
```

The `<what to check>` is the condition you want to check, if it satisfies (returns *true*), then it will do the `<do something>`.

Also, the `unless` will work if there's an `if` before it, like you want to check for multiple conditions, those structure are the same.

The `else` will work if all of the above `if` and `unless` returns a *false*.



### Fluentix Console

- Run: Run fluentix files (using current Fluentix Language available features)
- Packages: Will install addons for your Fluentix (still, WIP)
  + Download (will have install when the Fluentix Language has that function)
  + Reinstall (just remove that package and install it again)
  + Uninstall (remove that package)
  + Upload (Upload your packages: now just upload a dir, will be specified when Fluentix Language is finished; verify needs email)
  + Manage (Manages your uploaded packages; verify needs email)
- Alias: run long commands shorter

---

## Get Fluentix:

Get Fluentix via those ways:

### 1. All-in-one installer (coming soon)

It will be available in the future. https://fluentix.dev/get

### 2. Python

Install this zip, launch cmd/terminal and get into Fluentix's directory, unzip it and run the `setup.py` file with administration priveliges (mac: `sudo python setup.py` or windows (admin cmd): `python setup.py`)

If no errors occured, you have successfully installed Fluentix!

Start using it by typing `fluentix` (`flu` or `fl` for short)

## VS-Code:

Official syntax for Fluentix is at https://marketplace.visualstudio.com/manage/publishers/fluentix/extensions/fluentix/hub?_a=acquisition

---

## Community

If your interested, join us on discord here: https://discord.gg/mZNNfuMUVq

---

More features are promised to be added in near future!
