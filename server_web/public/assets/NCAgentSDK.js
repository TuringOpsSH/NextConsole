// sdk.js - 智能助手SDK核心代码
class NCAgentSDK {
    constructor(config) {
        this.config = {
            container: document.body, // 默认容器
            src: 'http://localhost:8080/sdk/app',
            width: '600px',
            height: '100vh',
            className: 'turing-agent-iframe',
            autoInit: false,
            extraData: {},
            ...config
        };
        this.iframe = null;
        this.iframeShow = false;
        this.readyHandler = null;
        this.messageHandler = null;
        this.lastConfig = null; // 保存上一次的配置
        if (this.config.autoInit) {
            this.init();
        }
    }
    // 比较两个配置对象是否相同（深度比较）
    _isConfigEqual(config1, config2) {
        if (config1?.token !== config2?.token) {
            return false;
        }
        if (config1?.appCode !== config2?.appCode) {
            return false;
        }
        if (config1?.sessionCode !== config2?.sessionCode) {
            return false;
        }
        if (config1?.taskCode !== config2?.taskCode) {
            return false;
        }
        if (JSON.stringify(config1?.workflowParams) !== JSON.stringify(config2?.workflowParams)) {
            return false;
        }
        if (config1?.question !== config2?.question) {
            return false;
        }
        if (config1?.autoAsk !== config2?.autoAsk) {
            return false;
        }
        if (JSON.stringify(config1?.extraData) !== JSON.stringify(config2?.extraData)) {
            return false;
        }
        return true;
    }

    // 初始化方法
    init() {
        if (!this.iframe) {
            // 创建iframe元素
            this.iframe = document.createElement('iframe');
            this.iframe.src = this.config.src;
            this.iframe.className = this.config.className;
            this.iframe.style.cssText = `
              width: ${this.config.width};
              height: ${this.config.height};
              border: none;
            `;
            // 添加到容器
            this.config.container.appendChild(this.iframe);
            // 设置消息监听器
            this.setupMessageHandlers();
            this.iframeShow = true;
            // 监听iframe加载完成
            this.iframe.onload = () => {
                console.log('Turing Agent iframe loaded successfully');
                if (this.config.onLoad) {
                    this.config.onLoad();
                }
            };
        }
        // 检查是否已有iframe且配置完全相同
        if (this._isConfigEqual(this.config, this.lastConfig)) {
            console.log('配置完全相同，无需重新初始化');
            return;
        }
        // 发送配置更新
        this._sendConfigUpdate();
        // 保存当前配置
        this.lastConfig = {...this.config};
    }

    // 发送配置更新
    _sendConfigUpdate() {
        if (!this.iframe || !this.iframe.contentWindow) return;

        this.iframe.contentWindow.postMessage(
            {
                type: 'SDK_CONFIG_UPDATE',
                token: this.config.token,
                appCode: this.config.appCode,
                sessionCode: this.config.sessionCode,
                workflowParams: this.config.workflowParams || {},
                taskCode: this.config.taskCode,
                question: this.config.question || '',
                autoAsk: this.config.autoAsk === true,
                extraData: this.config.extraData,
            },
            new URL(this.config.src).origin
        );
    }

    // 设置消息处理器
    setupMessageHandlers() {
        // 准备就绪处理器
        this.readyHandler = (event) => {
            if (event.data.type === 'SDK_RECEIVER_READY') {
                // 发送认证信息
                this.iframe.contentWindow.postMessage(
                    {
                        type: 'SDK_TOKEN_TRANSFER',
                        token: this.config.token,
                        appCode: this.config.appCode,
                        sessionCode: this.config.sessionCode,
                        workflowParams: this.config.workflowParams || {},
                        taskCode: this.config.taskCode,
                        question: this.config.question || '',
                        autoAsk: this.config.autoAsk === true,
                        extraData: this.config.extraData,
                    },
                    new URL(this.config.src).origin
                );
                console.log('Token sent after ready signal:', event.origin);
                // 移除一次性事件监听器
                window.removeEventListener('message', this.readyHandler);
                if (this.config.onReady) {
                    this.config.onReady(event);
                }
            }
        };

        // 通用消息处理器
        this.messageHandler = (event) => {
            // 确保消息来自预期的源
            if (new URL(this.config.src).origin !== event.origin) {
                return;
            }

            if (this.config.onMessage) {
                this.config.onMessage(event.data);
            }
        };

        // 添加事件监听
        window.addEventListener('message', this.readyHandler);
        window.addEventListener('message', this.messageHandler);
    }

    // 更新配置并重新初始化
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        this.init();
    }

    // 发送问题
    ask(question, autoAsk = true) {
        if (!this.iframe || !this.iframeShow) {
            console.error('Agent not initialized. Call init() first.');
            return;
        }

        this.iframe.contentWindow.postMessage(
            {
                type: 'SDK_QUESTION_ASK',
                question: question,
                autoAsk: autoAsk
            },
            new URL(this.config.src).origin
        );
    }

    // 销毁方法
    destroy() {
        if (this.iframe) {
            // 移除事件监听器
            if (this.readyHandler) {
                window.removeEventListener('message', this.readyHandler);
            }
            if (this.messageHandler) {
                window.removeEventListener('message', this.messageHandler);
            }

            // 移除iframe元素
            this.iframe.parentNode.removeChild(this.iframe);
            this.iframe = null;
        }

        this.iframeShow = false;

        if (this.config.onDestroy) {
            this.config.onDestroy();
        }

        console.log('Turing Agent destroyed successfully');
    }

    // 显示/隐藏助手
    toggle(show) {
        if (this.iframe) {
            this.iframe.style.display = show === undefined
                ? (this.iframe.style.display === 'none' ? 'block' : 'none')
                : (show ? 'block' : 'none');
        }
    }
}

// 全局访问
window.NCAgentSDK = NCAgentSDK;
export default NCAgentSDK;