{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = with pkgs; [
    imagemagick
    python312Packages.colorthief
    colorz
  ];
}
