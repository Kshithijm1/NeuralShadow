"use client";

import * as React from "react";
// import { Command } from "cmdk";
import { Search, FileText, Monitor, Mic, Cpu } from "lucide-react";
import { searchMemory, SearchResponse } from "../lib/api";
import { motion, AnimatePresence } from "framer-motion";

export function CommandMenu() {
    const [open, setOpen] = React.useState(false);
    const [search, setSearch] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const [result, setResult] = React.useState<SearchResponse | null>(null);

    const [mounted, setMounted] = React.useState(false);

    // Toggle with Cmd+K
    React.useEffect(() => {
        setMounted(true); // Hydration fix
        const down = (e: KeyboardEvent) => {
            if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
        };
        document.addEventListener("keydown", down);
        return () => document.removeEventListener("keydown", down);
    }, []);

    if (!mounted) return null;

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
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            {open && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                    onClick={() => setOpen(false)}
                />
            )}

            {/* Modal Content */}
            {open && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.1 }}
                    className="relative w-full max-w-2xl overflow-hidden rounded-xl border border-[#262626] bg-[#050505] shadow-2xl shadow-[#00ff9d]/10 ring-1 ring-[#00ff9d]/20"
                >
                    <div className="w-full flex flex-col">
                        <div className="flex items-center border-b border-[#262626] p-3">
                            <Search className="mr-3 h-5 w-5 text-gray-500" />
                            <input
                                autoFocus
                                placeholder="Ask Neural Shadow..."
                                value={search}
                                onChange={(e) => handleSearch(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') executeSearch();
                                }}
                                className="flex-1 bg-transparent text-lg text-[#ededed] placeholder:text-gray-600 outline-none"
                            />
                            {loading && <Cpu className="h-4 w-4 animate-spin text-[#00ff9d]" />}
                        </div>

                        <div className="max-h-[60vh] overflow-y-auto p-2">
                            {loading && (
                                <div className="py-6 text-center text-sm text-gray-500">
                                    Deciphering Neural Patterns...
                                </div>
                            )}

                            {!loading && !result && (
                                <div className="py-6 text-center text-sm text-gray-400">
                                    {search ? "No memory traces found." : "Type to query your digital ghost."}
                                </div>
                            )}

                            {result && (
                                <div className="space-y-4 p-2">
                                    {/* Answer */}
                                    <div className="rounded-lg border border-[#00ff9d]/30 bg-[#1a1a1a]/50 p-4">
                                        <h3 className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#00ff9d]">
                                            <Cpu size={14} /> Neural Core Answer
                                        </h3>
                                        <p className="leading-relaxed text-gray-200 text-sm">{result.answer}</p>
                                    </div>

                                    {/* Evidence */}
                                    <div className="space-y-2">
                                        <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500">Evidence Discovered</h4>
                                        {result.context.map((item) => (
                                            <div
                                                key={item.id}
                                                className="group relative flex cursor-pointer gap-3 rounded-md border border-transparent p-2 transition-colors hover:bg-white/5"
                                            >
                                                <div className="mt-1 text-[#00d9ff]">
                                                    {item.type === 'screen' ? <Monitor size={16} /> : <Mic size={16} />}
                                                </div>
                                                <div className="flex-1 overflow-hidden">
                                                    <div className="mb-1 flex items-center justify-between">
                                                        <span className="max-w-[200px] truncate font-mono text-xs text-[#00d9ff]">{item.source}</span>
                                                        <span className="text-[10px] text-gray-600">
                                                            {new Date(item.timestamp * 1000).toLocaleTimeString()}
                                                        </span>
                                                    </div>
                                                    <p className="line-clamp-2 text-sm text-gray-400 transition-colors group-hover:text-gray-200">
                                                        {item.text}
                                                    </p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
}
