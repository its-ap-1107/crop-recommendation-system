import PropTypes from 'prop-types'

export function Button({ children, type = "button", className = "", disabled = false, onClick }) {
  return (
    <button
      type={type}
      className={`px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
        disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors
        ${className}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

Button.propTypes = {
  children: PropTypes.node.isRequired,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  className: PropTypes.string,
  disabled: PropTypes.bool,
  onClick: PropTypes.func
} 