"use client";

import * as React from "react";
import { Command } from "cmdk";
import { Search, FileText, Monitor, Mic, Cpu } from "lucide-react";
import { searchMemory, SearchResponse } from "../lib/api";
import { motion, AnimatePresence } from "framer-motion";

export function CommandMenu() {
    const [open, setOpen] = React.useState(false);
    const [search, setSearch] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const [result, setResult] = React.useState<SearchResponse | null>(null);

    // Toggle with Cmd+K
    React.useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
        };
        document.addEventListener("keydown", down);
        return () => document.removeEventListener("keydown", down);
    }, []);

    const handleSearch = async (value: string) => {
        setSearch(value);
        // Simple debounce 
        // In prod, use a proper resize-observer or debounce lib
    };

    const executeSearch = async () => {
        if (!search) return;
        setLoading(true);
        const res = await searchMemory(search);
        setResult(res);
        setLoading(false);
    };

    return (
        <div className="fixed inset-0 pointer-events-none flex items-center justify-center z-50">
            {/* Dim Background */}
            {open && (
                <div className="absolute inset-0 bg-black/50 pointer-events-auto backdrop-blur-sm" onClick={() => setOpen(false)} />
            )}

            {/* Actual Command Menu - using the attribute selector from globals.css */}
            <Command
                data-open={open}
                className="pointer-events-auto"
                loop
            >
                <div className="flex items-center border-b border-[#262626] px-3">
                    <Search className="w-5 h-5 text-gray-500 mr-2" />
                    <Command.Input
                        placeholder="Ask Neural Shadow..."
                        value={search}
                        onValueChange={handleSearch}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') executeSearch();
                        }}
                    />
                    {loading && <Cpu className="w-4 h-4 text-[#00ff9d] animate-spin" />}
                </div>

                <Command.List>
                    {loading && <Command.Loading>Thinking...</Command.Loading>}

                    {!result && (
                        <Command.Empty>
                            {search ? "Press Enter to search..." : "Type to search your memory."}
                        </Command.Empty>
                    )}

                    {result && (
                        <div className="p-4 space-y-4">
                            {/* Answer Section */}
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="bg-[#1a1a1a]/50 p-4 rounded-lg border border-[#00ff9d]/30"
                            >
                                <h3 className="text-[#00ff9d] text-sm font-bold mb-2 uppercase tracking-wider flex items-center gap-2">
                                    <Cpu size={14} /> Neural Core Answer
                                </h3>
                                <p className="text-gray-200 leading-relaxed">{result.answer}</p>
                            </motion.div>

                            {/* Context Section */}
                            <div className="grid grid-cols-1 gap-2">
                                <h4 className="text-gray-500 text-xs font-bold uppercase tracking-wider mb-1">Evidence Discovered</h4>
                                {result.context.map((item) => (
                                    <Command.Item key={item.id} value={item.text} className="group">
                                        <div className="flex items-start gap-3 w-full p-2 hover:bg-white/5 rounded-md transition-colors cursor-pointer border border-transparent hover:border-[#00ff9d]/20">
                                            <div className="mt-1 text-[#00d9ff]">
                                                {item.type === 'screen' ? <Monitor size={16} /> : <Mic size={16} />}
                                            </div>
                                            <div className="flex-1 overflow-hidden">
                                                <div className="flex justify-between items-center mb-1">
                                                    <span className="text-xs text-[#00d9ff] font-mono truncate max-w-[200px]">{item.source}</span>
                                                    <span className="text-[10px] text-gray-600">
                                                        {new Date(item.timestamp * 1000).toLocaleTimeString()}
                                                    </span>
                                                </div>
                                                <p className="text-sm text-gray-400 line-clamp-2 group-hover:text-gray-200 transition-colors">
                                                    {item.text}
                                                </p>
                                            </div>
                                        </div>
                                    </Command.Item>
                                ))}
                            </div>
                        </div>
                    )}
                </Command.List>
            </Command>
        </div>
    );
}
