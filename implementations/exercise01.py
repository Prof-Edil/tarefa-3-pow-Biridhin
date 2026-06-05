import csv
import os

class Transaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = set(parents)
        self.children = set()

def main():
    txs = {}
    
    with open('data/mempool.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty lines or header
            if not row or row[0] == 'txid': 
                continue 
            
            txid = row[0]
            fee = int(row[1])
            weight = int(row[2])
            parents = row[3].split(';') if len(row) > 3 and row[3] else []
            txs[txid] = Transaction(txid, fee, weight, parents)

    # Map dependencies
    for txid, tx in txs.items():
        for p in tx.parents:
            if p in txs:
                txs[p].children.add(txid)

    block = []
    included = set()
    current_weight = 0
    current_fees = 0
    MAX_WEIGHT = 4000000

    # Handle the Mandatory Transaction
    mandatory_txid = '4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6'
    
    def get_all_ancestors(txid, ancestors_set):
        for p in txs[txid].parents:
            if p not in ancestors_set:
                get_all_ancestors(p, ancestors_set)
                ancestors_set.add(p)
        return ancestors_set

    mandatory_group = get_all_ancestors(mandatory_txid, set())
    mandatory_group.add(mandatory_txid)

    pending = list(mandatory_group)
    while pending:
        for txid in pending:
            if txs[txid].parents.issubset(included):
                block.append(txid)
                included.add(txid)
                current_weight += txs[txid].weight
                current_fees += txs[txid].fee
                pending.remove(txid)
                break

    # Maximize Fees
    eligible = set()
    for txid, tx in txs.items():
        if txid not in included and tx.parents.issubset(included):
            eligible.add(txid)

    print("Montando bloco...")
    while eligible:
        best_txid = max(eligible, key=lambda t: txs[t].fee / txs[t].weight)

        if current_weight + txs[best_txid].weight > MAX_WEIGHT:
            eligible.remove(best_txid)
            continue

        block.append(best_txid)
        included.add(best_txid)
        current_weight += txs[best_txid].weight
        current_fees += txs[best_txid].fee
        eligible.remove(best_txid)

        for child in txs[best_txid].children:
            if child not in included and txs[child].parents.issubset(included):
                eligible.add(child)

    # Output the results
    os.makedirs('solutions', exist_ok=True)
    output_path = 'solutions/exercise01.txt'
    with open(output_path, 'w') as f:
        for txid in block:
            f.write(f"{txid}\n")

    print(f"\nBloco montado com sucesso!")
    print(f"Total Weight: {current_weight:,} / {MAX_WEIGHT:,} vB")
    print(f"Total Fees:   {current_fees:,} sats")
    print(f"Transactions: {len(block):,}")

if __name__ == '__main__':
    main()