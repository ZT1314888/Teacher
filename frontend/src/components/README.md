# Components Usage

## Structure
- `layout/`: layout-level components (`AppHeader`, `SidebarNav`)
- `auth/`: auth page reusable containers (`AuthCard`, `AuthFooterLink`)
- `common/`: shared UI blocks (`PageHeader`, `LoadingState`, `EmptyState`, `ConfirmDialog`)
- `classroom/`: classroom domain components (`ClassroomFilterBar`, `ClassroomCard`)
- `reservation/`: reservation domain components (`ReservationStatusBadge`)

## Conventions
- All components use `script setup`.
- Shared styling relies on global utilities in `/Users/mac/Code/Django/Teacher/frontend/src/assets/styles/main.css`.
- Component-local style is kept in `<style scoped>`.
- Use `v-model` contract for stateful reusable components (`ConfirmDialog`, `ClassroomFilterBar`).

## Reuse Rules
- Page files should focus on data loading, actions, and routing.
- Repeated UI in 2+ pages must be promoted to `common/` or a domain folder.
