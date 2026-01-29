import { SolanaAgentKit } from "solana-agent-kit";
import TokenPlugin from "@solana-agent-kit/plugin-token";
import { Keypair, PublicKey } from "@solana/web3.js";
import bs58 from "bs58";
import dotenv from "dotenv";

dotenv.config();

export async function initializeAgent() {
  try {
    const privateKeyString = process.env.SOLANA_PRIVATE_KEY;
    
    if (!privateKeyString) {
      throw new Error("SOLANA_PRIVATE_KEY not found in .env");
    }

    const keypair = Keypair.fromSecretKey(bs58.decode(privateKeyString));

    const agent = new SolanaAgentKit(
      keypair,
      process.env.RPC_URL || "https://api.devnet.solana.com",
      {
        OPENAI_API_KEY: process.env.OLLAMA_API_KEY || "local"
      }
    )
      .use(TokenPlugin);

    console.log("[AGENT] Initialized successfully");
    console.log(`[AGENT] Wallet: ${keypair.publicKey.toString()}`);

    return agent;
  } catch (error) {
    console.error("[AGENT] Failed:", error.message);
    throw error;
  }
}

export async function autoTradeToken(agent, tokenMint, amount = 0.1) {
  try {
    console.log(`[TRADE] Executing for ${tokenMint}`);

    const signature = await agent.methods.trade(
      agent,
      new PublicKey(tokenMint),
      amount * 1000000000,
      new PublicKey("So11111111111111111111111111111111111111112"),
      300
    );

    console.log(`[TRADE] Success: ${signature}`);
    return signature;
  } catch (error) {
    console.error(`[TRADE] Failed: ${error.message}`);
    return null;
  }
}

export async function getTokenInfo(agent, tokenMint) {
  try {
    const info = await agent.methods.getTokenInfo(tokenMint);
    return info;
  } catch (error) {
    console.error(`[INFO] Failed: ${error.message}`);
    return null;
  }
}

