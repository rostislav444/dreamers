



export function randomColor(n: number){
    const colors = [
        'blue.50',
        'green.50',
        'red.50',
        'yellow.50',
        'purple.50',
    ]
    return colors[n % colors.length]
}