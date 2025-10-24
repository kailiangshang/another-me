import { useState, useEffect } from 'react';
import { Card, Typography, Row, Col, Statistic, Button, Space, Spin, Alert } from 'antd';
import { 
  FileTextOutlined, 
  MessageOutlined, 
  DatabaseOutlined,
  RocketOutlined,
  CheckCircleOutlined,
  WarningOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/api/client';
import { useConfigStore } from '@/store';

const { Title, Paragraph } = Typography;

export default function HomePage() {
  const navigate = useNavigate();
  const { config } = useConfigStore();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    documents: 0,
    messages: 0,
    memories: 0,
  });
  const [systemHealth, setSystemHealth] = useState<'healthy' | 'error' | 'unconfigured'>('unconfigured');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    try {
      // 检查系统健康
      const health = await apiClient.healthCheck();
      setSystemHealth(health.status === 'healthy' ? 'healthy' : 'error');

      // 加载统计数据
      if (config?.api_key) {
        const [ragStats, memStats] = await Promise.all([
          apiClient.getRAGStats().catch(() => ({ total_documents: 0 })),
          apiClient.getMemories(1).catch(() => ({ total: 0 })),
        ]);
        setStats({
          documents: ragStats.total_documents || 0,
          messages: 0, // TODO: 添加消息统计接口
          memories: memStats.total || 0,
        });
      }
    } catch (error) {
      console.error('Failed to load stats:', error);
      setSystemHealth('error');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div>
      {/* 顶部标题 */}
      <div style={{ marginBottom: 24 }}>
        <Title level={2} style={{ marginBottom: 8 }}>
          🌟 欢迎使用 Another Me
        </Title>
        <Paragraph style={{ fontSize: '16px', color: '#666' }}>
          基于 RAG 技术和记忆模仿的 AI 数字分身系统
        </Paragraph>
      </div>

      {/* 系统状态提示 */}
      {systemHealth === 'unconfigured' && (
        <Alert
          message="系统未配置"
          description="请先前往配置页面设置 API Key 后再使用"
          type="warning"
          icon={<WarningOutlined />}
          showIcon
          action={
            <Button size="small" onClick={() => navigate('/config')}>
              去配置
            </Button>
          }
          style={{ marginBottom: 24 }}
        />
      )}

      {systemHealth === 'healthy' && (
        <Alert
          message="系统运行正常"
          type="success"
          icon={<CheckCircleOutlined />}
          showIcon
          closable
          style={{ marginBottom: 24 }}
        />
      )}

      {/* 统计卡片 */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spin size="large" tip="加载统计信息..." />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={8}>
            <Card hoverable>
              <Statistic
                title="RAG 知识库"
                value={stats.documents}
                prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
                suffix="个文档"
                valueStyle={{ color: '#1890ff' }}
              />
              <Button 
                type="link" 
                size="small" 
                onClick={() => navigate('/knowledge')}
                style={{ marginTop: 8 }}
              >
                管理知识库 →
              </Button>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card hoverable>
              <Statistic
                title="MEM 对话"
                value={stats.messages}
                prefix={<MessageOutlined style={{ color: '#52c41a' }} />}
                suffix="条消息"
                valueStyle={{ color: '#52c41a' }}
              />
              <Button 
                type="link" 
                size="small" 
                onClick={() => navigate('/chat')}
                style={{ marginTop: 8 }}
              >
                开始对话 →
              </Button>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card hoverable>
              <Statistic
                title="记忆存储"
                value={stats.memories}
                prefix={<DatabaseOutlined style={{ color: '#fa8c16' }} />}
                suffix="条记忆"
                valueStyle={{ color: '#fa8c16' }}
              />
              <Button 
                type="link" 
                size="small" 
                onClick={() => navigate('/memory')}
                style={{ marginTop: 8 }}
              >
                查看记忆 →
              </Button>
            </Card>
          </Col>
        </Row>
      )}

      {/* 快速开始指引 */}
      <Card style={{ marginTop: 24 }}>
        <Title level={4}>
          <RocketOutlined /> 快速开始
        </Title>
        <Paragraph style={{ fontSize: '15px', lineHeight: '2' }}>
          <strong>1. 配置系统</strong><br />
          前往 <a onClick={() => navigate('/config')}>配置</a> 页面，设置你的 OpenAI API Key 和相关参数
          <br /><br />
          <strong>2. 构建知识库</strong><br />
          在 <a onClick={() => navigate('/knowledge')}>RAG 知识库</a> 上传你的文档、笔记、资料，构建专属知识库
          <br /><br />
          <strong>3. 开始对话</strong><br />
          在 <a onClick={() => navigate('/chat')}>MEM 对话</a> 与你的 AI 分身交流，它会模仿你的说话风格
        </Paragraph>
        <Space style={{ marginTop: 16 }}>
          <Button 
            type="primary" 
            icon={<RocketOutlined />}
            onClick={() => navigate(systemHealth === 'unconfigured' ? '/config' : '/chat')}
          >
            {systemHealth === 'unconfigured' ? '开始配置' : '开始对话'}
          </Button>
          <Button onClick={loadStats}>
            刷新统计
          </Button>
        </Space>
      </Card>

      {/* 功能介绍 */}
      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col xs={24} md={12}>
          <Card title="📚 RAG 知识管理">
            <Paragraph>
              • 上传个人文档、笔记、资料<br />
              • 智能检索和知识问答<br />
              • 知识库管理和统计分析
            </Paragraph>
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card title="💬 MEM 记忆模仿">
            <Paragraph>
              • 学习你的聊天记录和说话风格<br />
              • 模仿你的表达方式和思维模式<br />
              • 记忆管理和时间线展示
            </Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
