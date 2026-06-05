import hashlib
import os

def sha256(data: bytes) -> bytes:
    """Retorna o hash SHA-256 simples dos bytes brutos de entrada."""
    return hashlib.sha256(data).digest()

def build_merkle_tree_and_proof(txids_hex, target_txid_hex):
    # Strings para bytes
    current_level = [bytes.fromhex(txid) for txid in txids_hex]
    target_leaf = bytes.fromhex(target_txid_hex)
    
    # Encontra o índice da transação alvo
    try:
        idx = current_level.index(target_leaf)
    except ValueError:
        raise ValueError("A transação alvo não foi encontrada na lista fornecida.")
        
    proof = []
    
    # Constrói a Merkle Tree de baixo para cima
    while len(current_level) > 1:
        next_level = []
        
        # Duplica último nó se num de nós for ímpar
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])
            
        sibling_idx = idx + 1 if idx % 2 == 0 else idx - 1
        proof.append(current_level[sibling_idx].hex())
        
        # Combina os hashes em pares
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]
            
            combined = left + right
            next_level.append(sha256(combined))
            
        idx //= 2
        current_level = next_level
        
    merkle_root = current_level[0].hex()
    
    return merkle_root, proof

def main():
    input_file = 'data/ex02_txid_list.txt'
    try:
        with open(input_file, 'r') as f:
            txids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Arquivo {input_file} não encontrado.")
        return

    target_txid = "49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb"
    
    print(f"Construindo a Merkle Tree para {len(txids)} transações...")
    root, proof = build_merkle_tree_and_proof(txids, target_txid)
    
    print(f"Merkle Root: {root}")
    print(f"Tamanho da Prova: {len(proof)} níveis")
    
    os.makedirs('solutions', exist_ok=True)
    output_file = 'solutions/exercise02.txt'
    with open(output_file, 'w') as f:
        f.write(root + '\n')
        for p in proof:
            f.write(p + '\n')

if __name__ == '__main__':
    main()