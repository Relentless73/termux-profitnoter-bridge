export type TermuxManifestFile = {
  path: string;
  extension?: string;
};

export type TermuxManifest = {
  format?: string;
  root_name?: string;
  files?: TermuxManifestFile[];
};

export type ImportedTermuxNote = {
  title: string;
  category: "Other";
  body: string;
};

export function manifestToNote(manifest: TermuxManifest): ImportedTermuxNote {
  if (manifest.format !== "profitnoter.termux-manifest.v1" || !Array.isArray(manifest.files)) {
    throw new Error("Unsupported Termux manifest");
  }

  const grouped = manifest.files.reduce<Record<string, string[]>>((groups, file) => {
    const extension = file.extension || "no extension";
    (groups[extension] ||= []).push(file.path);
    return groups;
  }, {});

  const lines = Object.entries(grouped)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([extension, paths]) => `${extension}: ${paths.slice(0, 20).join(", ")}${paths.length > 20 ? ` (+${paths.length - 20} more)` : ""}`);

  return {
    title: `Termux inventory — ${manifest.root_name || "workspace"}`,
    category: "Other",
    body: [
      `Safe inventory imported from Termux. ${manifest.files.length} visible file(s).`,
      "",
      ...lines,
      "",
      "Only filenames and metadata were imported. Script contents, archives, credentials, tokens, cookies, and MCP configuration were excluded.",
    ].join("\n"),
  };
}
