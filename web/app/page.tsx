import { CommandMenu } from "@/components/CommandMenu";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center relative overflow-hidden">
      {/* Background Visuals */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-transparent to-[#050505] pointer-events-none" />

      {/* Content */}
      <div className="z-10 text-center space-y-6">
        <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#00ff9d] to-[#00d9ff] drop-shadow-[0_0_15px_rgba(0,255,157,0.5)]">
          NEURAL SHADOW
        </h1>
        <p className="text-gray-400 text-lg max-w-md mx-auto">
          System Online. Passive Capture Active.
        </p>

        <div className="inline-flex items-center gap-2 px-4 py-2 bg-[#1a1a1a] rounded-full border border-[#262626] text-sm text-gray-400 mt-8 hover:border-[#00ff9d] transition-colors cursor-default">
          <kbd className="font-mono bg-[#262626] px-2 py-1 rounded text-white text-xs">Cmd</kbd>
          <span>+</span>
          <kbd className="font-mono bg-[#262626] px-2 py-1 rounded text-white text-xs">K</kbd>
          <span>to search memory</span>
        </div>
      </div>

      {/* The Search Interface */}
      <CommandMenu />
    </main>
  );
}
