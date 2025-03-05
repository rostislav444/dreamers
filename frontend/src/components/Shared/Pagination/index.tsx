import { Box, Button, Flex, Text } from "@chakra-ui/react";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  hasNext: boolean;
  hasPrevious: boolean;
}

export const Pagination = ({ 
  currentPage, 
  totalPages, 
  onPageChange,
  hasNext,
  hasPrevious
}: PaginationProps) => {
  if (totalPages <= 1) return null;

  const renderPageButtons = () => {
    const pageButtons = [];
    const maxButtonsToShow = 5;
    
    // Calculate range of pages to show
    let startPage = Math.max(1, currentPage - Math.floor(maxButtonsToShow / 2));
    let endPage = Math.min(totalPages, startPage + maxButtonsToShow - 1);
    
    // Adjust start page if we're near the end
    if (endPage - startPage + 1 < maxButtonsToShow) {
      startPage = Math.max(1, endPage - maxButtonsToShow + 1);
    }
    
    // Add first page button with ellipsis if needed
    if (startPage > 1) {
      pageButtons.push(
        <Button 
          key="first" 
          onClick={() => onPageChange(1)}
          variant={1 === currentPage ? "solid" : "outline"}
          colorScheme="blue"
          mx={1}
          size="sm"
        >
          1
        </Button>
      );
      
      if (startPage > 2) {
        pageButtons.push(<Text key="ellipsis1" mx={1}>...</Text>);
      }
    }
    
    // Add page buttons
    for (let i = startPage; i <= endPage; i++) {
      pageButtons.push(
        <Button 
          key={i} 
          onClick={() => onPageChange(i)}
          variant={i === currentPage ? "solid" : "outline"}
          colorScheme="blue"
          mx={1}
          size="sm"
        >
          {i}
        </Button>
      );
    }
    
    // Add last page button with ellipsis if needed
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pageButtons.push(<Text key="ellipsis2" mx={1}>...</Text>);
      }
      
      pageButtons.push(
        <Button 
          key="last" 
          onClick={() => onPageChange(totalPages)}
          variant={totalPages === currentPage ? "solid" : "outline"}
          colorScheme="blue"
          mx={1}
          size="sm"
        >
          {totalPages}
        </Button>
      );
    }
    
    return pageButtons;
  };

  return (
    <Box mt={8} mb={4}>
      <Flex justifyContent="center" alignItems="center">
        <Button
          isDisabled={!hasPrevious}
          onClick={() => onPageChange(currentPage - 1)}
          mr={2}
          variant="outline"
          size="sm"
        >
          Предыдущая
        </Button>
        
        {renderPageButtons()}
        
        <Button
          isDisabled={!hasNext}
          onClick={() => onPageChange(currentPage + 1)}
          ml={2}
          variant="outline"
          size="sm"
        >
          Следующая
        </Button>
      </Flex>
    </Box>
  );
};