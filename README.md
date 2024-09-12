# 🌈 `pywal-nix`

> Extremely straightforward evaluation-time Pywal integration for Home Manager

`pywal-nix` is focused on providing the simplest way of integrating custom
Pywal colourschemes into any Home Manager configuration at evaluation-time.

I needed a pure (not `--impure`) Nix solution. I made a pure Nix solution. It
works well. I'll likely hack on it some more, even though I personally only use
the `wal` backend.

## Usage

### Flake

Add `pywal-nix` to your flake inputs.

```nix
{
  inputs = {
    pywal-nix = {
      url = "github:Fuwn/pywal-nix";
      inputs.nixpkgs.follows = "nixpkgs"; # Recommended
    };
  };
}
```

### Home Manager

After adding `pywal-nix` to your flake inputs, consume it as a Home Manager
module.

```nix
# ...

inputs.home-manager.lib.homeManagerConfiguration {
  modules = [
    inputs.pywal-nix.${pkgs.system}.homeManagerModules.default
  ];
};

# ...
```

Finally, configure and access `pywal-nix` in your Home Manager configuration through
the `pywal-nix` attribute.

```nix
{ pkgs, config, ... }:
{
  # Configuration
  pywal-nix = {
    wallpaper = /path/to/wallpaper.png; # Required
    light = false;                      # Defaults to false
  };

  # Example usage to print out two colourscheme colours
  home.packages = [
    (pkgs.writeShellScriptBin "colourscheme-sample" ''
      echo '${config.pywal-nix.colourscheme.colour0} ${config.pywal-nix.colourscheme.colour15}'
    '')
  ];
}
```

## Pywal

This project combines the
[`pywal/backends/wal.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/wal.py)
and
[`pywal/util.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/util.py)
files from [dylanaraps/pywal](https://github.com/dylanaraps/pywal) into the
[`wal.py`](./wal.py) file. Pywal is licensed under the
[MIT License](https://github.com/dylanaraps/pywal/blob/master/LICENSE.md).

## Licence

This project is licensed with the [GNU General Public License v3.0](./LICENSE).
