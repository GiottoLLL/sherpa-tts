import React, { useState } from "react"
import { Layout, Menu, Typography, Space } from "antd"
import { SoundOutlined, HistoryOutlined, HomeOutlined } from "@ant-design/icons"
import TTSForm from "./components/TTSForm"
import HistoryList from "./components/HistoryList"
import "./App.css"

const { Header, Content, Sider } = Layout
const { Title, Text } = Typography

type MenuKey = "tts" | "history"

const App: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = useState<MenuKey>("tts")

  // 菜单项配置
  const menuItems = [
    {
      key: "tts",
      icon: <SoundOutlined />,
      label: "语音合成"
    },
    {
      key: "history", 
      icon: <HistoryOutlined />,
      label: "历史记录"
    }
  ]

  // 渲染主要内容
  const renderContent = () => {
    switch (selectedMenu) {
      case "tts":
        return <TTSForm />
      case "history":
        return <HistoryList />
      default:
        return <TTSForm />
    }
  }

  return (
    <Layout style={{ minHeight: "100vh" }}>
      {/* 侧边栏 */}
      <Sider
        width={250}
        style={{
          background: "#fff",
          borderRight: "1px solid #f0f0f0"
        }}
      >
        {/* Logo区域 */}
        <div style={{ 
          padding: "24px 16px", 
          borderBottom: "1px solid #f0f0f0",
          textAlign: "center"
        }}>
          <Space direction="vertical" size="small">
            <HomeOutlined style={{ fontSize: "32px", color: "#1890ff" }} />
            <Title level={4} style={{ margin: 0, color: "#1890ff" }}>
              Sherpa TTS
            </Title>
            <Text type="secondary" style={{ fontSize: "12px" }}>
              文字转语音系统
            </Text>
          </Space>
        </div>

        {/* 导航菜单 */}
        <Menu
          mode="inline"
          selectedKeys={[selectedMenu]}
          items={menuItems}
          onClick={({ key }) => setSelectedMenu(key as MenuKey)}
          style={{ 
            border: "none",
            paddingTop: "16px"
          }}
        />
      </Sider>

      {/* 主要内容区域 */}
      <Layout>
        {/* 顶部标题栏 */}
        <Header 
          style={{ 
            background: "#fff", 
            padding: "0 24px",
            borderBottom: "1px solid #f0f0f0",
            display: "flex",
            alignItems: "center"
          }}
        >
          <Title level={3} style={{ margin: 0 }}>
            {selectedMenu === "tts" ? "语音合成" : "历史记录"}
          </Title>
        </Header>

        {/* 内容区域 */}
        <Content
          style={{
            margin: "24px",
            padding: "24px",
            background: "#f5f5f5",
            borderRadius: "8px",
            overflow: "auto"
          }}
        >
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  )
}

export default App