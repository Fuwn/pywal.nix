# 🌈 `pywal.nix`

> Extremely straightforward evaluation-time Pywal integration for Home Manager

`pywal.nix` is focused on providing the simplest way of integrating custom
Pywal colour schemes into any Home Manager configuration at evaluation-time.

I needed a pure (not `--impure`) Nix solution. I made a pure Nix solution. It
works well.

## Installation

### Standalone Home-Manager

```nix
{ pkgs, ... }:
{
  imports = [
    (import (
      pkgs.fetchFromGitHub {
        owner = "Fuwn";
        repo = "pywal.nix";
        rev = "...";  # Use the current commit revision hash
        hash = "..."; # Use the current commit sha256 hash
      }
    )).homeManagerModules.${builtins.currentSystem}.default
  ];
}
```

> You can use projects like [nurl](https://github.com/nix-community/nurl) and
> [`nix-prefetch`](https://github.com/msteen/nix-prefetch) to simplify the
> usage of `fetchFromGitHub`.

### Flakes & Home-Manager

Add `pywal.nix` to your flake inputs.

```nix
{
  inputs.pywal-nix = {
    url = "github:Fuwn/pywal.nix";
    inputs.nixpkgs.follows = "nixpkgs"; # Recommended
  };
}
```

After adding `pywal.nix` to your flake inputs, consume it as a Home Manager
module.

```nix
# ...

inputs.home-manager.lib.homeManagerConfiguration {
  modules = [
    inputs.pywal-nix.homeManagerModules.${pkgs.system}.default
  ];
};

# ...
```

## Configuration & Usage

Configure and access `pywal.nix` in your Home Manager configuration through the
`pywal-nix` attribute.

```nix
{ pkgs, config, ... }:
{
  # Configuration
  pywal-nix = {
    wallpaper = /path/to/wallpaper.png; # Required
    light = false;                      # Defaults to false
    backend = "wal";                    # One of "colorthief", "colorz",
                                        # "fast_colorthief", "haishoku",
                                        # "schemer2", "wal"; Default to "wal"
    enableKittyIntegration = true;      # Defaults to true
  };

  # Example usage to print out few colours
  home.packages = [
    (pkgs.writeShellScriptBin "colour-scheme-sample" ''
      echo '${config.pywal-nix.colourScheme.wallpaper}'
      echo '${config.pywal-nix.colourScheme.special.background}'
      echo '${config.pywal-nix.colourScheme.colours.colour9}'
    '')
  ];
}
```

### Colour Scheme

`pywal.nix`'s generated colour scheme is accessible through either the
`colourScheme` or `colorScheme` set. Likewise, colours are accessible through
either the `colours` or `colors` sets.

The colour scheme interface generated by `pywal.nix` comes in the following shape:

```typescript
{
  wallpaper: string

  special: {
    background: string
    foreground: string
    cursor: string
  }

  colours: { // or colors
    colour0: string // or color0
    // colour1 ... colour14 or color1 ... color15
    colour15: string // or color15
  }
}
```

## Pywal

This project includes multiple files from
[dylanaraps/pywal](https://github.com/dylanaraps/pywal), a project which is
licensed under the [MIT License](./pywal/LICENSE.md).

- [`pywal/backends/colorthief.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/colorthief.py)
- [`pywal/backends/colorz.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/colorz.py)
- [`pywal/backends/fast_colorthief.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/fast_colorthief.py)
- [`pywal/backends/haishoku.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/haishoku.py)
- [`pywal/backends/schemer2.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/schemer2.py)
- [`pywal/backends/wal.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/backends/wal.py)
- [`pywal/colors.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/colors.py)
- [`pywal/theme.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/theme.py)
- [`pywal/util.py`](https://github.com/dylanaraps/pywal/blob/master/pywal/util.py)

## Licence

This project is licensed with the [GNU General Public License v3.0](./LICENSE).
