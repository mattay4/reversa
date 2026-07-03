// Fonte única da regra de não-destrutividade do Reversa: as únicas pastas em
// que o framework pode criar/escrever. Renderiza o texto da regra injetado em
// cada arquivo de entrada de engine no momento do install.
//
// `_reversa_sdd` e `_reversa_forward` são configuráveis pelo usuário
// (state.json: output_folder / forward_folder). `_reversa_docs` é fixo por
// enquanto; se um dia virar configurável (docs_folder), basta passá-lo aqui.

// Exportada também para uso futuro por updateGitignore/uninstall, que hoje
// só conhecem `.reversa/` + output_folder e divergem da regra global.
export function getWritableFolders({
  outputFolder = '_reversa_sdd',
  forwardFolder = '_reversa_forward',
} = {}) {
  return ['.reversa/', `${outputFolder}/`, '_reversa_docs/', `${forwardFolder}/`];
}

export function renderPolicyBlock(opts = {}) {
  const folders = getWritableFolders(opts).map((f) => `\`${f}\``);
  const list = `${folders.slice(0, -1).join(', ')} e ${folders[folders.length - 1]}`;
  return [
    'Nunca apague, modifique ou sobrescreva arquivos pré-existentes do projeto legado.',
    `O Reversa escreve apenas em ${list}.`,
  ].join('\n');
}
