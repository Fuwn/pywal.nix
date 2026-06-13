{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    systems.url = "github:nix-systems/default";
    flake-compat.url = "https://flakehub.com/f/edolstra/flake-compat/1.tar.gz";

    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };

    pre-commit-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      pre-commit-hooks,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      homeManagerModules.default =
        { config, ... }:
        let
          inherit (pkgs) lib;

          pkgs = import nixpkgs { inherit system; };

          colourScheme = builtins.fromJSON (
            builtins.readFile "${
              pkgs.runCommand "colour-scheme"
                {
                  buildInputs = with pkgs; [
                    imagemagick
                    jq
                    (pkgs.python3.withPackages (ps: [
                      ps.colorthief
                      ps.numpy
                      ps.pillow
                      (ps.buildPythonPackage rec {
                        pname = "haishoku";
                        version = "1.1.8";
                        format = "setuptools";
                        doCheck = false;

                        src = ps.fetchPypi {
                          inherit pname version;
                          hash = "sha256-5LmhTANYYIGxirzwS0MgFo/qk/9hHoGyvM1dUmn/y9Q=";
                        };
                      })
                      (ps.buildPythonPackage {
                        pname = "fast_colorthief";
                        version = "0.0.5";
                        format = "setuptools";
                        doCheck = false;
                        dontUseCmakeConfigure = true;

                        # The vendored CMakeLists.txt requests a pre-3.5 policy
                        # version, which modern CMake refuses outright.
                        env.CMAKE_POLICY_VERSION_MINIMUM = "3.5";

                        nativeBuildInputs = [
                          pkgs.cmake
                          ps.setuptools
                          ps.setuptools-scm
                          ps.scikit-build
                        ];

                        src = pkgs.fetchgit {
                          url = "https://github.com/bedapisl/fast-colorthief";
                          rev = "92eda78157bed309ef9c12e85708ae21241e11d0";
                          hash = "sha256-0S8YI2DlEMx75vuAxcWzTBCcerLvULdh4nY2k3zdsqg=";
                          fetchSubmodules = true;
                        };
                      })
                      (ps.buildPythonPackage rec {
                        pname = "colorz";
                        version = "1.0.3";
                        format = "setuptools";
                        doCheck = false;

                        propagatedBuildInputs = [
                          ps.pillow
                          ps.scipy
                        ];

                        src = ps.fetchPypi {
                          inherit pname version;

                          hash = "sha256-wE/2OJYoHy7hMnvN/y52ozn3BVmr2KJdKMDR+yhIDT4=";
                        };
                      })
                    ]))
                    (pkgs.buildGoModule {
                      pname = "schemer2";
                      version = "89a66cbf40440e82921719c6919f11bb563d7cfa";
                      vendorHash = null;

                      src = pkgs.fetchFromGitHub {
                        owner = "thefryscorer";
                        repo = "schemer2";
                        rev = "89a66cbf40440e82921719c6919f11bb563d7cfa";
                        hash = "sha256-EKjVz4NkxtxqGissFwlzUahFut9UAxS8icxx3V7aNnw=";
                      };

                      postPatch = ''
                        printf 'module github.com/Fuwn/schemer2\n\ngo 1.22.5\n' > go.mod
                      '';
                    })
                  ];
                }
                ''
                  mkdir -p $out/wrapper

                  cp ${./wrap.py} $out/wrapper/wrap.py
                  cp -r ${./pywal} $out/wrapper/pywal

                  python3 $out/wrapper/wrap.py ${config.pywal-nix.backend} ${config.pywal-nix.wallpaper} ${
                    if config.pywal-nix.light then "1" else "0"
                  } | \
                    sed "s/'/\"/g" | \
                    jq 'to_entries | map({"colour\(.key)": .value, "color\(.key)": .value}) | add' > $out/colour-scheme
                ''
            }/colour-scheme"
          );
        in
        {
          options.pywal-nix = {
            wallpaper = lib.mkOption {
              type = lib.types.path;
              default = /path/to/wallpaper.png;
            };

            backend = lib.mkOption {
              type = lib.types.enum [
                "colorthief"
                "colorz"
                "fast_colorthief"
                "haishoku"
                "schemer2"
                "wal"
              ];

              default = "wal";
            };

            light = lib.mkOption {
              type = lib.types.bool;
              default = false;
            };

            colourScheme = lib.mkOption {
              type = lib.types.anything;
            };

            colorScheme = lib.mkOption {
              type = lib.types.anything;
            };

            enableKittyIntegration = lib.mkOption {
              type = lib.types.bool;
              default = true;
            };
          };

          config = {
            pywal-nix.colourScheme = {
              inherit (config.pywal-nix) wallpaper;

              colours = colourScheme;
              colors = colourScheme;

              special = {
                background = colourScheme.colour0;
                foreground = colourScheme.colour15;
                cursor = colourScheme.colour15;
              };
            };

            pywal-nix.colorScheme = config.pywal-nix.colourScheme;
          };

          config.programs.kitty.extraConfig = lib.mkIf config.pywal-nix.enableKittyIntegration ''
            foreground ${config.pywal-nix.colourScheme.special.foreground}
            background ${config.pywal-nix.colourScheme.special.background}
            cursor ${config.pywal-nix.colourScheme.special.cursor}
            color0 ${config.pywal-nix.colourScheme.colours.colour0}
            color1 ${config.pywal-nix.colourScheme.colours.colour1}
            color2 ${config.pywal-nix.colourScheme.colours.colour2}
            color3 ${config.pywal-nix.colourScheme.colours.colour3}
            color4 ${config.pywal-nix.colourScheme.colours.colour4}
            color5 ${config.pywal-nix.colourScheme.colours.colour5}
            color6 ${config.pywal-nix.colourScheme.colours.colour6}
            color7 ${config.pywal-nix.colourScheme.colours.colour7}
            color8 ${config.pywal-nix.colourScheme.colours.colour8}
            color9 ${config.pywal-nix.colourScheme.colours.colour9}
            color10 ${config.pywal-nix.colourScheme.colours.colour10}
            color11 ${config.pywal-nix.colourScheme.colours.colour11}
            color12 ${config.pywal-nix.colourScheme.colours.colour12}
            color13 ${config.pywal-nix.colourScheme.colours.colour13}
            color14 ${config.pywal-nix.colourScheme.colours.colour14}
            color15 ${config.pywal-nix.colourScheme.colours.colour15}
          '';
        };

      formatter = nixpkgs.legacyPackages."${system}".nixfmt-rfc-style;

      checks.pre-commit-check = pre-commit-hooks.lib.${system}.run {
        src = ./.;

        hooks = {
          deadnix.enable = true;
          flake-checker.enable = true;
          nixfmt-rfc-style.enable = true;
          statix.enable = true;
        };
      };

      devShells.default = nixpkgs.legacyPackages.${system}.mkShell {
        inherit (self.checks.${system}.pre-commit-check) shellHook;

        buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
      };
    });
}
