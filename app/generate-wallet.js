import { Keypair } from "@solana/web3.js";
import bs58 from "bs58";
import fs from "fs";

const keypair = Keypair.generate();

console.log("=".repeat(50));
console.log("NEW DEVNET WALLET GENERATED");
console.log("=".repeat(50));
console.log("Public Key:", keypair.publicKey.toString());
console.log("=".repeat(50));
console.log("Private Key (Base58):");
console.log(bs58.encode(keypair.secretKey));
console.log("=".repeat(50));

fs.writeFileSync("devnet-wallet.json", JSON.stringify(Array.from(keypair.secretKey)));
console.log("Wallet saved to devnet-wallet.json");
console.log("\nCopy the Private Key above to your .env file");
