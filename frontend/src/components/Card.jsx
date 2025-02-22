import PropTypes from 'prop-types'

export function Card({ children, className = "" }) {
  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {children}
    </div>
  )
}

Card.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string
} 