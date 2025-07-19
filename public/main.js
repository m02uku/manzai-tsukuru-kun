// 履歴保存用
let history = [];
// 履歴をlocalStorageから復元
if (window.localStorage) {
    try {
        const saved = localStorage.getItem("manzai_history");
        if (saved) {
            history = JSON.parse(saved);
        }
    } catch (e) {}
}
// ページロード時に履歴を表示
window.addEventListener("DOMContentLoaded", function () {
    updateHistory();
});
let lastScript = "";

document.getElementById("gemini-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    // 必須項目取得
    const refComedian = document.getElementById("ref-comedian").value.trim();
    const nameA = document.getElementById("name-a").value.trim();
    const nameB = document.getElementById("name-b").value.trim();
    const theme = document.getElementById("theme").value.trim();
    // バリデーション（漫才師名はオプショナルに変更）
    if (!refComedian || !theme) {
        document.getElementById("response").textContent =
            "必須項目（参考漫才師・テーマ）をすべて入力してください。";
        return;
    }
    // オプショナル項目取得
    const combination = document.getElementById("combination").value.trim();
    const style = document.getElementById("style").value;
    const roleA = document.getElementById("role-a").value;
    const roleB = document.getElementById("role-b").value;
    const character = document.getElementById("character").value.trim();
    const audience = document.getElementById("audience").value.trim();
    const ngWord = document.getElementById("ng-word").value.trim();
    // 構成項目削除
    const language = document.getElementById("language").value.trim();
    const funny = document.getElementById("funny").value;

    // プロンプト生成（全項目必ず含める・空欄は{指定なし}）
    let prompt = `参考漫才師: ${refComedian || "{指定なし}"}`;
    let aLine = "A:";
    aLine += nameA ? ` ${nameA}` : " {指定なし}";
    aLine += roleA ? ` (${roleA})` : " (役割:{指定なし})";
    prompt += `\n${aLine}`;
    let bLine = "B:";
    bLine += nameB ? ` ${nameB}` : " {指定なし}";
    bLine += roleB ? ` (${roleB})` : " (役割:{指定なし})";
    prompt += `\n${bLine}`;
    prompt += `\nテーマ: ${theme || "{指定なし}"}`;
    prompt += `\nコンビ名: ${combination || "{指定なし}"}`;
    prompt += `\nスタイル: ${style || "{指定なし}"}`;
    prompt += `\n口調・キャラクター: ${character || "{指定なし}"}`;
    prompt += `\nターゲット観客層: ${audience || "{指定なし}"}`;
    prompt += `\nNGワード・避けたい話題: ${ngWord || "{指定なし}"}`;
    // オチのタイプは削除
    // 構成項目削除
    prompt += `\n使用言語（e.g. 標準語、関西弁）: ${language || "{指定なし}"}`;
    prompt += `\n面白さの度合い（1-10）: ${funny || "{指定なし}"}`;
    // デバッグ用: ユーザー入力プロンプトのみをコンソール出力
    console.log("[Gemini User Prompt]", prompt);

    const responseDiv = document.getElementById("response");
    responseDiv.textContent = "応答を取得中...";
    try {
        const res = await fetch("/api/gemini", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: prompt }),
        });
        const data = await res.json();
        if (res.status === 429 && data.wait_seconds !== undefined) {
            responseDiv.textContent = `${data.error}\n残り待ち時間: ${data.wait_seconds}秒`;
        } else {
            // Geminiの出力の改行をHTMLで正しく表示する
            if (data.output) {
                responseDiv.innerHTML = data.output.replace(/\n/g, "<br>");
            } else {
                responseDiv.textContent = data.error || "応答がありません";
            }
            if (data.output) {
                lastScript = data.output;
                history.unshift(data.output);
                updateHistory();
                document.getElementById("download-btn").style.display = "inline-block";
            }
        }
    } catch (err) {
        responseDiv.textContent = "エラーが発生しました";
    }
});

function updateHistory() {
    const historyUl = document.getElementById("history");
    historyUl.innerHTML = "";
    history.forEach((item, idx) => {
        const li = document.createElement("li");
        li.textContent = `No.${history.length - idx}: ${item.substring(0, 30)}...`;
        li.style.cursor = "pointer";
        li.onclick = () => {
            document.getElementById("response").innerHTML = item.replace(/\n/g, "<br>");
            lastScript = item;
        };
        historyUl.appendChild(li);
    });
    // 履歴をlocalStorageに保存
    if (window.localStorage) {
        try {
            localStorage.setItem("manzai_history", JSON.stringify(history));
        } catch (e) {}
    }
}

document.getElementById("download-btn").addEventListener("click", function () {
    if (!lastScript) return;
    // タイトル抽出（---の直後の「タイトル:」行を探す）
    let title = "manzai_script";
    const match = lastScript.match(/---\s*\n(?:.|\n)*?\nタイトル: ?(.+)\n/);
    if (match && match[1]) {
        // ファイル名に使えない文字を除去
        title = match[1].replace(/[\\/:*?"<>|\n]/g, "_").trim();
        if (!title) title = "manzai_script";
    }
    const blob = new Blob([lastScript], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title}.txt`;
    a.click();
    URL.revokeObjectURL(url);
});
