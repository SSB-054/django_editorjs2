class linkbutton {
    static get toolbox() {
        return {
            title: "Button",
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12.034 12.681a.498.498 0 0 1 .647-.647l9 3.5a.5.5 0 0 1-.033.943l-3.444 1.068a1 1 0 0 0-.66.66l-1.067 3.443a.5.5 0 0 1-.943.033z"/><path d="M21 11V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6"/></svg>'
        }
    }
    constructor({
        data: t,
        api: e
    }) {
        this.api = e;
        const defaultValues = window?.LinkButtonDefaultThemes || {
            color: "#ecf0f1",
            background: "#2980b9",
            borderColor: "#34495e"
        };
        this.data = {
            title: t.title || "",
            description: t.description || "",
            link: t.link || "#",
            color: t.color || defaultValues.color,
            backgroundColor: t.backgroundColor || defaultValues.background,
            borderColor: t.borderColor || defaultValues.borderColor
        };

        this.redraw = () => { };
    }
    render() {
        this.data;
        const t = document.createElement("div");
        t.classList.add("cdx-block"), t.classList.add("cdx-button-links"), t.style.margin = "8px auto", t.style.display = "flex", t.style.flexDirection = "column", t.style.gap = "4px", t.style.padding = "12px";
        const e = document.createElement("div");
        e.classList.add("cdx-input"), e.contentEditable = !0, e.innerText = this.data.title, e.setAttribute("data-placeholder", "Button Title");
        const o = document.createElement("div");
        o.classList.add("cdx-input"), o.contentEditable = !0, o.innerText = this.data.description, o.setAttribute("data-placeholder", "Button Description");
        const r = document.createElement("div");
        r.classList.add("cdx-input"), r.contentEditable = !0, r.innerText = this.data.description, r.setAttribute("data-placeholder", "https://example.com"), t.style.color = this.data.color, t.style.fontFamily = this.data.fontFamily;
        const n = document.createElement("div"),
            a = () => {
                this.data.title = e.innerText || "Untitled", this.data.description = o.innerText, this.data.link = r.innerText || "#", n.innerHTML = `\n<div style="color: var(--grayText);font-size: small;margin: 4px auto;">Preview</div>\n<a target="_blank" href="${this.data.link}" role="button" style="\nborder: 1px solid ${this.data.borderColor};\nbackground: ${this.data.backgroundColor};\nborder-radius: 8rem;\nbox-shadow: 0 4px 6px -1px ${this.data.borderColor}, 0 2px 4px -1px rgba(0, 0, 0, 0.06);\nbox-sizing: border-box;\ncursor: pointer;\ntext-decoration: none;\ndisplay: flex;\nflex-direction: column;\nalign-items: center;\ncolor: ${this.data.color || "black"};\njustify-content: center;\nline-height: 1.15;\ntext-align: center;\nappearance: button;\npadding: 8px;\nwidth: 100%;">\n<strong>${this.data.title}</strong>\n<span style="font-size: smaller;">${this.data.description || "Insert a text.."}</span>\n            </a>`
            };
        return e.addEventListener("input", a), o.addEventListener("input", a), r.addEventListener("input", a), a(), this.redraw = a, t.appendChild(e), t.appendChild(o), t.appendChild(r), t.appendChild(n), t
    }
    save(t) {
        return this.data
    }
    renderSettings() {
        const t = window?.LinkButtonThemes || {
            default: {
                color: "#ecf0f1",
                background: "#2980b9",
                borderColor: "#34495e"
            },
            "corporate-blue": {
                "color": "#ffffff",
                "background": "#2c3e80",
                "borderColor": "#34495e"
            },
            "executive-gray": {
                "color": "#f8f9fa",
                "background": "#425563",
                "borderColor": "#2c3e50"
            },
            "professional-navy": {
                "color": "#ffffff",
                "background": "#1f4e79",
                "borderColor": "#2c3e50"
            },
            "ocean-breeze": {
                "color": "#ffffff",
                "background": "#3498db",
                "borderColor": "#2980b9"
            },
            "sunset-warmth": {
                "color": "#ecf0f1",
                "background": "#e67e22",
                "borderColor": "#d35400"
            },
            "earthy-moss": {
                "color": "#ffffff",
                "background": "#8bc34a",
                "borderColor": "#7cb342"
            },

        };

        const e = document.createElement("div");
        return e.innerHTML = '<span class="ce-popover-item__title" style="margin-right: 4px;">Color</span>', e.style.display = "flex", e.style.flexWrap = "wrap", e.style.gap = "2px", e.style.padding = "4px", Object.keys(t).forEach((o => {
            const r = document.createElement("div");
            r.classList.add("ce-popover-item"),
                function (e, o) {
                    const r = t[o];
                    r ? (e.style.color = r.color, e.style.backgroundColor = r.background, e.style.borderColor = r.borderColor) : console.error(`Theme '${o}' not found`)
                }(r, o), r.style.width = "16px", r.style.height = "16px", r.style.borderRadius = "4px", r.style.cursor = "pointer", r.addEventListener("click", (() => {
                    const e = t[o];
                    this.data.color = e.color, this.data.backgroundColor = e.background, this.data.borderColor = e.borderColor, this.redraw()
                })), e.appendChild(r)
        })), e
    }
}