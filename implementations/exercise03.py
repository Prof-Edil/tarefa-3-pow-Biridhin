import hashlib
import multiprocessing
import time
import os

VERSION = "00000002"
PREV_BLOCK = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"

MERKLE_ROOT = "c0a692de10b69e2381a2856dcb0d0736dcd307bf25af7ce74831bf25793de626" 

TIMESTAMP = "495f8f09" 
TARGET = 0x00000000ffff0000000000000000000000000000000000000000000000000000

def mine_worker(args):
    start_nonce, step, prefix_hex = args
    nonce = start_nonce
    
    prefix_bytes = bytes.fromhex(prefix_hex)
    
    while True:
        # Formata o Nonce em 8 bytes
        nonce_bytes = nonce.to_bytes(8, byteorder='big')
        
        # Junta os blocos
        header_bytes = prefix_bytes + nonce_bytes
        
        # Hash único SHA-256
        h = hashlib.sha256(header_bytes).digest()
        
        if h[:4] == b'\x00\x00\x00\x00':
            if int.from_bytes(h, 'big') <= TARGET:
                return header_bytes.hex(), h.hex(), nonce
                
        nonce += step

def main():
    # Cabeçalho
    prefix_hex = VERSION + PREV_BLOCK + MERKLE_ROOT + TIMESTAMP
    
    cores = multiprocessing.cpu_count()
    print(f"Minerando com {cores} threads em paralelo.")
    
    start_time = time.time()
    
    with multiprocessing.Pool(cores) as pool:
        args = [(i, cores, prefix_hex) for i in range(cores)]
        
        for result in pool.imap_unordered(mine_worker, args):
            if result:
                header_hex, hash_hex, nonce = result
                elapsed = time.time() - start_time
                
                print(f"Proof of Work Válido!")
                print(f"Tempo de Mineração: {elapsed:.2f} segundos")
                print(f"Hash Vencedor:      {hash_hex}")
                print(f"Nonce utilizado:    {nonce} (0x{nonce:016x})")
                
                os.makedirs('solutions', exist_ok=True)
                with open('solutions/exercise03.txt', 'w') as f:
                    f.write(header_hex)
                    
                pool.terminate()
                break

if __name__ == '__main__':
    main()