import { useState, useRef, useEffect } from 'react';
import { Input, Button, List, Card, Typography, message, Spin } from 'antd';
import { SendOutlined, DeleteOutlined } from '@ant-design/icons';
import { useChatStore } from '@/store';
import apiClient from '@/api/client';

const { TextArea } = Input;
const { Title } = Typography;

export default function ChatPage() {
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const { messages, addMessage, clearMessages } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim()) {
      message.warning('请输入消息');
      return;
    }

    const userMessage = {
      role: 'user' as const,
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    addMessage(userMessage);
    setInputValue('');
    setLoading(true);

    try {
      const response = await apiClient.chatSync(userMessage.content);
      addMessage({
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
      });
    } catch (error: any) {
      message.error(error.response?.data?.detail || '发送失败，请检查配置');
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    clearMessages();
    message.success('对话已清空');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={2} style={{ margin: 0 }}>MEM 对话</Title>
        <Button 
          icon={<DeleteOutlined />} 
          onClick={handleClear}
          disabled={messages.length === 0}
        >
          清空对话
        </Button>
      </div>
      
      <Card 
        style={{ 
          flex: 1,
          marginBottom: 16, 
          overflow: 'auto',
          display: 'flex',
          flexDirection: 'column'
        }}
        bodyStyle={{ flex: 1, overflow: 'auto' }}
      >
        {messages.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px 20px',
            color: '#999'
          }}>
            <p style={{ fontSize: '16px', marginBottom: '8px' }}>💬 开始与 AI 分身对话</p>
            <p style={{ fontSize: '14px' }}>它会模仿你的说话风格回答</p>
          </div>
        ) : (
          <>
            <List
              dataSource={messages}
              renderItem={(item, index) => (
                <List.Item
                  key={index}
                  style={{
                    padding: '12px 0',
                    border: 'none'
                  }}
                >
                  <div style={{ width: '100%' }}>
                    <div style={{
                      display: 'inline-block',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      maxWidth: '80%',
                      backgroundColor: item.role === 'user' ? '#1890ff' : '#f0f0f0',
                      color: item.role === 'user' ? 'white' : 'black',
                      float: item.role === 'user' ? 'right' : 'left',
                      clear: 'both'
                    }}>
                      <div style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                        {item.content}
                      </div>
                      <div style={{ 
                        fontSize: '12px', 
                        opacity: 0.7,
                        marginTop: '4px'
                      }}>
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </List.Item>
              )}
            />
            <div ref={messagesEndRef} />
          </>
        )}
        {loading && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin tip="AI 思考中..." />
          </div>
        )}
      </Card>

      <Input.Group compact style={{ display: 'flex' }}>
        <TextArea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="输入消息（Shift+Enter 换行，Enter 发送）..."
          autoSize={{ minRows: 2, maxRows: 4 }}
          onPressEnter={(e) => {
            if (!e.shiftKey && !loading) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
          style={{ flex: 1 }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          loading={loading}
          onClick={handleSend}
          disabled={!inputValue.trim()}
          style={{ height: 'auto', minWidth: '100px' }}
        >
          发送
        </Button>
      </Input.Group>
    </div>
  );
}
