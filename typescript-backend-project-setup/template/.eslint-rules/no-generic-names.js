module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Forbid generic names (Utils, Helper, Service, Handler, etc) in filenames, class names, and exports',
      recommended: true,
    },
  },
  create(context) {
    const filename = context.getFilename()

    const forbiddenWords = ['utils', 'helpers', 'helper', 'service', 'services', 'manager', 'managers', 'processor', 'processors', 'data']
    const forbiddenPattern = new RegExp(
      `(^|/)(${ forbiddenWords.join('|') })(\.ts$|\.tsx$|/|$)`,
      'i'
    )

    const isForbiddenName = (name) => {
      if (!name) return false

      return forbiddenWords.some(word => {
        const lowerName = name.toLowerCase()
        return (
          lowerName === word ||
          lowerName.startsWith(word) ||
          lowerName.endsWith(word)
        )
      })
    }

    const violations = []

    if (forbiddenPattern.test(filename)) {
      violations.push({
        type: 'filename',
        message: `Generic filename or path. Use domain-specific naming (e.g., NodePositioner.ts, EdgeRenderer.ts)`,
      })
    }

    return {
      ClassDeclaration(node) {
        if (node.id && isForbiddenName(node.id.name)) {
          context.report({
            node: node.id,
            message: `Generic class name "${ node.id.name }". Use domain purpose (e.g., NodePositioner, EdgeRenderer, OrderValidator)`,
          })
        }
      },

      Program(node) {
        if (forbiddenPattern.test(filename)) {
          context.report({
            node,
            message: `Generic filename or path. Use domain-specific naming (e.g., NodePositioner.ts, EdgeRenderer.ts)`,
          })
        }
      },
    }
  },
}
