export function addSpacesToNumber(number: number): string {
  const formattedNumber = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  return formattedNumber;
}