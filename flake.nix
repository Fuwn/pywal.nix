{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    {
      nixpkgs,
      systems,
      ...
    }:
    (nixpkgs.lib.genAttrs (import systems)) (system: {
      homeManagerModules.default =
        { config, ... }:
        let
          inherit (pkgs) lib;

          pkgs = import nixpkgs { inherit system; };

          colourscheme = builtins.fromJSON (
            builtins.readFile "${
              pkgs.runCommand "colourscheme"
                {
                  buildInputs = with pkgs; [
                    imagemagick
                    jq
                    python312Packages.colorthief
                    colorz
                  ];
                }
                ''
                  mkdir -p $out/wrapper

                  cp ${./wrap.py} $out/wrapper/wrap.py
                  cp -r ${./pywal} $out/wrapper/pywal

                  ${pkgs.python3}/bin/python3 $out/wrapper/wrap.py ${config.pywal-nix.backend} ${config.pywal-nix.wallpaper} ${
                    if config.pywal-nix.light then "1" else "0"
                  } | \
                    sed "s/'/\"/g" | \
                    jq 'to_entries | map({"colour\(.key)": .value}) | add' > $out/colourscheme
                ''
            }/colourscheme"
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
                "wal"
              ];

              default = "wal";
            };

            light = lib.mkOption {
              type = lib.types.bool;
              default = false;
            };

            colourscheme = lib.mkOption {
              type = lib.types.attrsOf lib.types.str;
            };
          };

          config.pywal-nix.colourscheme = colourscheme;
        };
    });
}
