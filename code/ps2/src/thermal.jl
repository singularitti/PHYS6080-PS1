function temperature(particles)
    N = length(particles)
    velocities = map(Base.Fix2(getfield, :v), particles)
    return 16 / N * sum(abs2, velocities)
end

volume(particles) = length(particles) / ρ
