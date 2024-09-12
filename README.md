# 🌈 `pywal-nix`

> Extremely straightforward evaluation-time Pywal integration for Home Manager

`pywal-nix` is focused on providing the simplest way of integrating custom
Pywal colour schemes into any Home Manager configuration at evaluation-time.

I needed a pure (not `--impure`) Nix solution. I made a pure Nix solution. It
works well.

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
    backend = "wal";                    # One of "wal", "colorz", or "colorthief"; Defaults to "wal"
  };

  # Example usage to print out two colour scheme colours
  home.packages = [
    (pkgs.writeShellScriptBin "colour-scheme-sample" ''
      echo '${config.pywal-nix.colourScheme.colour0} ${config.pywal-nix.colourScheme.colour15}'
    '')
  ];
}
```

## Pywal

This project includes multiple files from
[dylanaraps/pywal](https://github.com/dylanaraps/pywal), a project which is
licensed under the [MIT License](./pywal/LICENSE.md).

- [`pywal/backends/colorthief.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/colorthief.py)
- [`pywal/backends/colorz.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/colorz.py)
- [`pywal/backends/wal.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/wal.py)
- [`pywal/colors.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/colors.py)
- [`pywal/theme.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/theme.py)
- [`pywal/util.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/util.py)

## Licence

This project is licensed with the [GNU General Public License v3.0](./LICENSE).
