# voltha-utils

This repo contains a set of scripts and configurations that I created over time while working on VOLTHA.

I suggest to add the `scripts` folder to you path so that you can execute them from everywhere.

You can do that with:

```shell
echo "export PATH=\$PATH:$(pwd)/scripts" >> ~/.bashrc
```

_NOTE if you are a Mac user you probably won't to add that to `.bash_profile` instead of `.bashrc`_

## Usage

As of now most of the scripts in this repo assume that they live side to side with
the `voltha-helm-charts` folder.

For example to deploy `voltha` (on `master` with custom images and `ingresses` set up) you can run:

```shell
kind create cluster --name voltha-dev --config configs/voltha-dev-cluster-kind.cfg
voltha-deploy -w att -f configs/values/dev-values.yaml
```

_The two parameters reported here are the default ones, so feel free to remove or customize them._

**This repo is unmaintened and undocumented. For more information about the scripts look into the code :)**
