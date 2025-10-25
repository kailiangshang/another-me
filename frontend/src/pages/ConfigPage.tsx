import { useState, useEffect } from 'react';
import { Form, Input, Button, Card, Typography, message, Space, Alert, Divider } from 'antd';
import { SaveOutlined, CheckCircleOutlined, ApiOutlined } from '@ant-design/icons';
import { useConfigStore } from '@/store';
import apiClient from '@/api/client';
import type { APIConfig } from '@/types';

const { Title } = Typography;

export default function ConfigPage() {
  const [form] = Form.useForm();
  const [testing, setTesting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);
  const { config, setConfig } = useConfigStore();

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const savedConfig = await apiClient.loadConfig();
      if (savedConfig) {
        form.setFieldsValue(savedConfig);
        setConfig(savedConfig);
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  };

  const handleTest = async () => {
    try {
      const values = await form.validateFields();
      setTesting(true);
      setTestResult(null);
      
      const result = await apiClient.testConfig(values);
      setTestResult(result);
      
      if (result.success) {
        message.success('配置测试成功!');
      } else {
        message.error(result.message || '配置测试失败');
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || '配置测试失败';
      setTestResult({ success: false, message: errorMsg });
      message.error(errorMsg);
    } finally {
      setTesting(false);
    }
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setSaving(true);
      
      const result = await apiClient.saveConfig(values);
      
      if (result.success) {
        setConfig(values);
        message.success('配置保存成功!');
        // 清除测试结果
        setTestResult(null);
      } else {
        message.error(result.message || '配置保存失败');
      }
    } catch (error: any) {
      message.error(error.response?.data?.detail || '配置保存失败');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <Title level={2}>
        <ApiOutlined /> 系统配置
      </Title>
      <Paragraph style={{ color: '#666', fontSize: '15px' }}>
        配置 OpenAI API 相关参数，支持 OpenAI 和其他兼容 API
      </Paragraph>

      {/* 配置提示 */}
      <Alert
        message="配置说明"
        description={
          <div>
            <p>• API Key: 你的 OpenAI API 密钥，以 sk- 开头</p>
            <p>• Base URL: API 服务地址，默认为 OpenAI 官方地址</p>
            <p>• Model: 使用的模型名称，如 gpt-3.5-turbo、gpt-4 等</p>
          </div>
        }
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Card style={{ maxWidth: 600 }}>
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            base_url: 'https://api.openai.com/v1',
            model: 'gpt-3.5-turbo',
          }}
        >
          <Form.Item
            label="API Key"
            name="api_key"
            rules={[
              { required: true, message: '请输入 API Key' },
              { pattern: /^sk-/, message: 'API Key 应以 sk- 开头' }
            ]}
            extra="你的 OpenAI API 密钥，将被安全存储"
          >
            <Input.Password 
              placeholder="sk-..." 
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item
            label="API Base URL"
            name="base_url"
            rules={[
              { required: true, message: '请输入 Base URL' },
              { type: 'url', message: '请输入有效的 URL' }
            ]}
            extra="默认为 OpenAI 官方地址，也可使用代理服务"
          >
            <Input placeholder="https://api.openai.com/v1" />
          </Form.Item>

          <Form.Item
            label="模型"
            name="model"
            rules={[{ required: true, message: '请输入模型名称' }]}
            extra="推荐使用 gpt-3.5-turbo 或 gpt-4"
          >
            <Input placeholder="gpt-3.5-turbo" />
          </Form.Item>

          <Divider />

          {/* 测试结果 */}
          {testResult && (
            <Alert
              message={testResult.success ? '测试成功' : '测试失败'}
              description={testResult.message}
              type={testResult.success ? 'success' : 'error'}
              showIcon
              closable
              onClose={() => setTestResult(null)}
              style={{ marginBottom: 16 }}
            />
          )}

          <Form.Item style={{ marginBottom: 0 }}>
            <Space>
              <Button
                type="default"
                icon={<CheckCircleOutlined />}
                onClick={handleTest}
                loading={testing}
              >
                测试配置
              </Button>
              <Button
                type="primary"
                icon={<SaveOutlined />}
                onClick={handleSave}
                loading={saving}
              >
                保存配置
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {/* 常见问题 */}
      <Card title="常见问题" style={{ marginTop: 24, maxWidth: 600 }}>
        <div style={{ lineHeight: 2 }}>
          <p><strong>Q: 如何获取 API Key？</strong></p>
          <p>A: 访问 <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer">OpenAI Platform</a> 注册并创建 API Key</p>
          
          <p><strong>Q: 可以使用国内代理吗？</strong></p>
          <p>A: 可以，只需将 Base URL 修改为代理服务的地址即可</p>
          
          <p><strong>Q: 配置保存在哪里？</strong></p>
          <p>A: 配置保存在后端服务器上，不会泄露到浏览器</p>
        </div>
      </Card>
    </div>
  );
}
