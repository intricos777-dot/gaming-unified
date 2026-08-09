#!/usr/bin/env bash
set -euo pipefail
echo '=== layered debug ==='
node -e "import('./src/layered-enochian.js').then(m=>console.log('format:', m.status()))"
echo
echo '--- smoke seal/unseal ---'
TMP=$(mktemp)
HOME_TMP=$(mktemp -d)
mkdir -p "$HOME_TMP/.quantum-enochian-layered/keys" "$HOME_TMP/.quantum-enochian-layered/sealed"
ORIG_HOME="$HOME"
export HOME="$HOME_TMP"
SECRET="${QE_TEST_SECRET:-user-only-secret}"
CONTEXT='smoke-test'
echo 'plaintext' > "$TMP.in"
node "$HOME/Projects/quantum-enochian/src/layered-cli.js" seal --input "$TMP.in" --secret "$SECRET" --context "$CONTEXT" --name smoke >/dev/null
node "$HOME/Projects/quantum-enochian/src/layered-cli.js" unseal --input "$HOME/Projects/quantum-enochian/.quantum-enochian-layered/sealed/smoke.sealed" --secret "$SECRET" --context "$CONTEXT"
export HOME="$ORIG_HOME"
rm -rf "$HOME_TMP" "$TMP" "$TMP.in"
echo
echo '--- layer diagnostics ---'
for i in $(seq 0 6); do
  name=$(node -e "import('./src/layered-enochian.js').then(m=>console.log(m.LAYER_NAMES[$i]))")
  echo "Layer ${i}: ${name}"
done
