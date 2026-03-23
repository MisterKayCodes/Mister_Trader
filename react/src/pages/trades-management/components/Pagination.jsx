import React from 'react';

import Button from '../../../components/ui/Button';
import Select from '../../../components/ui/Select';

const Pagination = ({ currentPage, totalPages, pageSize, onPageChange, onPageSizeChange, totalItems }) => {
  const pageSizeOptions = [
    { value: '10', label: '10 per page' },
    { value: '25', label: '25 per page' },
    { value: '50', label: '50 per page' },
    { value: '100', label: '100 per page' }
  ];

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    
    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages?.push(i);
      }
    } else {
      if (currentPage <= 3) {
        for (let i = 1; i <= 4; i++) pages?.push(i);
        pages?.push('...');
        pages?.push(totalPages);
      } else if (currentPage >= totalPages - 2) {
        pages?.push(1);
        pages?.push('...');
        for (let i = totalPages - 3; i <= totalPages; i++) pages?.push(i);
      } else {
        pages?.push(1);
        pages?.push('...');
        for (let i = currentPage - 1; i <= currentPage + 1; i++) pages?.push(i);
        pages?.push('...');
        pages?.push(totalPages);
      }
    }
    
    return pages;
  };

  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <div className="flex flex-col lg:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-4 w-full lg:w-auto">
          <span className="text-sm text-muted-foreground whitespace-nowrap">
            Showing {startItem}-{endItem} of {totalItems}
          </span>
          <div className="w-full sm:w-40">
            <Select
              options={pageSizeOptions}
              value={pageSize?.toString()}
              onChange={(value) => onPageSizeChange(parseInt(value))}
            />
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            iconName="ChevronLeft"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
          />
          
          <div className="hidden sm:flex items-center gap-1">
            {getPageNumbers()?.map((page, index) => (
              page === '...' ? (
                <span key={`ellipsis-${index}`} className="px-2 text-muted-foreground">...</span>
              ) : (
                <Button
                  key={page}
                  variant={currentPage === page ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => onPageChange(page)}
                  className="min-w-[40px]"
                >
                  {page}
                </Button>
              )
            ))}
          </div>

          <div className="sm:hidden">
            <span className="px-4 py-2 text-sm font-medium text-foreground">
              {currentPage} / {totalPages}
            </span>
          </div>

          <Button
            variant="outline"
            size="sm"
            iconName="ChevronRight"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          />
        </div>
      </div>
    </div>
  );
};

export default Pagination;