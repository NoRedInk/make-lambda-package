{ pkgs ? import <nixpkgs> {}
}:
pkgs.mkShell {
  buildInputs = [ pkgs.pipenv ];
  shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
  '';
}
