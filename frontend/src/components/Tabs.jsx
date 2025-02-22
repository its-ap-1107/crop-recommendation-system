import { useState } from 'react'
import PropTypes from 'prop-types'

export function Tabs({ defaultTab, children }) {
  const [activeTab, setActiveTab] = useState(defaultTab)
  
  const tabs = children.filter(child => child.type === TabPanel)
  
  return (
    <div>
      <div className="flex space-x-2 mb-4 border-b">
        {tabs.map((tab) => (
          <button
            key={tab.props.value}
            onClick={() => setActiveTab(tab.props.value)}
            className={`px-4 py-2 font-medium transition-colors
              ${activeTab === tab.props.value 
                ? 'text-blue-600 border-b-2 border-blue-600' 
                : 'text-gray-600 hover:text-blue-600'}`}
          >
            {tab.props.label}
          </button>
        ))}
      </div>
      {tabs.find(tab => tab.props.value === activeTab)}
    </div>
  )
}

Tabs.propTypes = {
  defaultTab: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired
}

export function TabPanel({ children, value }) {
  return (
    <div role="tabpanel" id={`panel-${value}`}>
      {children}
    </div>
  )
}

TabPanel.propTypes = {
  children: PropTypes.node.isRequired,
  value: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired
} 