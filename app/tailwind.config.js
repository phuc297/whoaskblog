// module.exports = {
//     purge: {
//         enabled: false,
//         content: [
//             './**/templates/*.html',
//             './**/templates/**/*.html',
//             './**/*.js',
//             './**/*.jsx',
//             './**/*.ts',
//             './**/*.tsx',
//         ]
//     },
//     theme: {
//         extend: {
//             height: {
//                 '64': '16rem',
//                 '80': '20rem',
//             },
//             borderRadius: {
//                 '4xl': '2rem',
//             }
//         },
//     },
//     variants: {},
//     plugins: [],
// }

/** @type {import('tailwindcss').Config} */
module.exports = {
    important: true,
    content: [
        './**/templates/*.html',
        './**/templates/**/*.html',
        './**/*.js',
        './**/*.jsx',
        './**/*.ts',
        './**/*.tsx',],
    plugins: [],
    theme: {
        extend: {
            height: {
                '64': '16rem',
                '80': '20rem',
            }
        }
    }
}