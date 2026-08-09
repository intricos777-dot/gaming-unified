# Quantum Enochian — Layered Format

Alternate layered encryption format with 7 user-specific keyed layers, self-healing/debug wrappers, and BDE patrol.

## Format
- `forward-seal` encrypts plaintext through all 7 layers
- `reverse-unseal` decrypts through all 7 layers in reverse
- Each layer uses its own name + user secret + context in key derivation
- Layer keys are derived on-the-fly; no persistent key material required for normal use
- Stored personal layer keys live under `~/.quantum-enochian-layered/keys/`

## 7 Layers
1. Root — spirit
2. Veil — earth
3. Sigil — water
4. Aethyr — air
5. Choir — fire
6. Watchtower — spirit
7. Seal — earth

## Usage
```bash
node src/layered-cli.js status
node src/layered-cli.js seal --input secret.txt --secret '<USER_SECRET>' --context 'project-x'
node src/layered-cli.js unseal --input sealed.txt --secret '<USER_SECRET>' --context 'project-x'
node src/layered-cli.js keygen --layer 4 --name 'my-mental-layer' --entropy /path/to/entropy-file
```

## Self-Heal / Debug / Patrol
```bash
bash scripts/self-heal-layered.sh
bash scripts/debug-layered.sh
bash scripts/bde-layered-patrol.sh
```

## Personal Layer Keys
Only you should know the mapping between layer indexes and your personal layer secrets. Record them offline and never commit them.
